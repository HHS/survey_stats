import us
import pandas as pd
import numpy as np
from cytoolz.itertoolz import unique
from cytoolz.functoolz import thread_last, identity
from cytoolz.curried import map, filter, curry
from survey_stats import pdutil
# import sys
# import traceback as tb


from survey_stats import log


logger = log.getLogger(__name__)


US_STATES_FIPS_INTS = thread_last(
    us.STATES_AND_TERRITORIES,
    map(lambda x: x.fips),
    filter(lambda x: x is not None),
    map(lambda x: int(x)),
    list
)


SITECODE_TRANSLATORS = {'fips':
                        lambda x: (us.states.lookup('%.2d' % x).abbr if
                                   int(x) in US_STATES_FIPS_INTS else 'NA'),
                        'codes': identity}

SVYDESIGN_COLS = ['sitecode', 'strata', 'psu', 'weight']


def convert_cat_codes(s, fmt):
    unq_lvls = list(unique(
        [fmt[k] for k in sorted(fmt.keys())]
    ))
    c = (pd.to_numeric(s, downcast='integer')
         .astype('category')
         .pipe(lambda xf: xf.cat.rename_categories(
             [fmt[k] for k in sorted(xf.unique().dropna())]))
         .cat.set_categories(unq_lvls))
    return c


def convert_cat_force(s, fmt):
    unq_lvls = list(unique(
        [fmt[k] for k in sorted(fmt.keys())]
    ))
    c = (pd.to_numeric(s, downcast='integer')
         .replace(to_replace=fmt)
         .astype('category')
         .cat.set_categories(unq_lvls))
    return c


def eager_convert(s, fmt, lgr=logger):
    c = s
    try:
        c = convert_cat_codes(s, fmt)
        lgr.info('converted series with fmt', v=s.name, fmt=fmt,
                  levels=s.value_counts().to_dict(), new_levels=c.value_counts().to_dict())
    except ValueError as e:
        lgr.info('ValueError converting to category! Forcing...',
                 err=e, col=s.name, fmt=fmt, levels=s.value_counts().to_dict())
        c = convert_cat_force(s, fmt)
    except KeyError as e:
        lgr.info('KeyError casting to cat, check var labels! Passing...',
                 err=e, col=s.name, fmt=fmt, levels=s.value_counts().to_dict())
    return c


def eager_convert_categorical(s, lbls, fmts, lgr=logger):
    fmt = None
    if s.name in lbls.keys():
        fmt = lbls[s.name]
        lgr.debug('formatted with lbls', v=s.name)
    elif s.name in fmts:
        fmt = fmts[s.name]
        lgr.info('found missing format to patch', v=s.name, fmt=fmt,
                 levels=s.value_counts().to_dict())
    if not fmt:
        lgr.debug('could not find fmt for var, skipping', v=s.name)
        return s
    return eager_convert(s, fmt, lgr)


def filter_columns(df, facets, qids, lgr=logger):
    # should drop columns w/ facet names
    # unless the mapped value is the same
    # drop_cols = set(facets.keys()).difference(facets.values())
    # include columns in qids and facets
    fcols = set(qids).union(facets.keys())
    # iff they are found in this sub-df and not in drop_cols
    cols = sorted(fcols.intersection(df.columns))  # .difference(drop_cols))
    ndf = df[cols]
    lgr.info('filtered df columns using facets, qids',
             old_shape=df.shape, new_shape=ndf.shape,
             missing=fcols.difference(cols), f=facets, cols=cols)
    return ndf


def find_na_synonyms(na_syns, df):
    df = df.applymap(
        lambda x: np.nan if
        (x.lower() in na_syns if type(x) == str else False)
        else x)
    logger.info("replaced NA synonyms", shp=df.shape)
    return df


def munge_df(df, r, lbls, facets, qids, na_syns, col_fn, fmts, fpc=False, lgr=logger):
    year = r['year']
    lgr.bind(year=year)
    lgr.info('filtering, applying varlabels, munging', patch_fmts=fmts.keys(), colfn=col_fn, shp=df.shape, lbls=lbls)
    # get mapping into table for each facet
    facets = {r[k]: k for k in facets}
    if not qids:
        qids = list(set(lbls.keys()).difference(
                    [r['sitecode'], r['year'], r['weight'], r['psu'], r['strata']] +
                    [k for k in facets]))
    ncols = {k: k.lower() for k in list(df.columns)}
    ndf = (df.rename(index=str, columns=ncols)
           .pipe(lambda xdf: filter_columns(xdf, facets, qids))
           .reset_index(drop=True)
           .apply(lambda x: eager_convert_categorical(x, lbls, fmts, lgr))
           .rename(index=str, columns=facets)
           .pipe(curry(find_na_synonyms)(na_syns))
           .reset_index(drop=True)
           .assign(year=int(year) if type(year) == int else df[year].astype(int),
                   sitecode=df[r['sitecode']].apply(
                       SITECODE_TRANSLATORS[r['sitecode_type']]).astype('category'),
                   weight=df[r['weight']].astype(float),
                   strata=df[r['strata']].astype(int),
                   psu=df[r['psu']].astype(int))
           .reset_index(drop=True))
    if fpc:
        ndf = (ndf.assign(fpc=df[r['fpc']].astype(float),
                         sample_ct=df[r['sample_ct']].astype(int))
                  .reset_index(drop=True))
    ndf.columns = list(map(pdutil.undash, list(ndf.columns)))
    lgr.info('completed SAS df munging')
    lgr.unbind('year')
    return ndf
