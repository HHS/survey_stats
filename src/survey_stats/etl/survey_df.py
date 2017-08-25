import sys
import us
import pandas as pd
import numpy as np
from cytoolz.itertoolz import mapcat
from cytoolz.functoolz import thread_last
from cytoolz.curried import map, filter, curry
import traceback as tb
import dask
from dask import distributed as dd
from dask import delayed
from dask import bag
from dask.distributed import Client


from survey_stats import log
from survey_stats import pdutil


logger = log.getLogger(__name__)


US_STATES_FIPS_INTS = thread_last(
    us.STATES_AND_TERRITORIES,
    map(lambda x: x.fips),
    filter(lambda x: x is not None),
    map(lambda x: int(x)),
    list
)

SITECODE_TRANSLATORS = {
    'fips': lambda x: (us.states.lookup('%.2d' % x).abbr if
                       int(x) in US_STATES_FIPS_INTS else 'NA')
}

SVYDESIGN_COLS = ['sitecode', 'strata', 'psu', 'weight']

def force_convert_categorical(s, lbls):
    c = (pd.to_numeric(s.fillna(-1), downcast='integer')
         .replace(to_replace=lbls[s.name])
         .astype('category'))
    return c


def eager_convert_categorical(s, lbls):
    if not s.name in lbls.keys():
        return s
    try:
        c = (pd.to_numeric(s, downcast='integer')
             .astype('category')
             .pipe(lambda xf: xf.cat.rename_categories(
                        [lbls[s.name][k] for k in
                         sorted(xf.unique().dropna())]))
             .cat.set_categories(
                [lbls[s.name][k] for k in sorted(lbls[s.name].keys())])
             .astype('category'))
        return c
    except KeyError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        xcep = tb.format_exception(exc_type,exc_value, exc_traceback)
        logger.warning('KeyError casting to cat, check var labels! Passing...',
                       err=e, col=s.name, v=s.value_counts().to_dict())
        return s
    except ValueError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.warning('ValueError converting to category! Forcing...',
                       err=e, v=s.value_counts().to_dict())
        return force_convert_categorical(s, lbls)


def filter_columns(df, facets, qids):
    # should drop columns w/ facet names
    # unless the mapped value is the same
    drop_cols = set(facets.values()).difference(facets.keys())

    # include columns in qids and facets
    fcols = set(qids).union(facets.values())

    # iff they are found in this sub-df and not in drop_cols
    cols = sorted(fcols.intersection(df.columns).difference(drop_cols))

    ndf = df[cols]
    logger.info('filtered df columns using facets, qids',
                old_shape=df.shape, new_shape=ndf.shape,
                missing=fcols.difference(cols), dropped=drop_cols)
    return ndf


def find_na_synonyms(na_syns, df):
    df = df.applymap(
        lambda x: np.nan if
        (x.lower() in na_syns if type(x) == str else False)
        else x)
    return df

def undash(col):
    return 'x' + col if col[0] == '_' else col

def munge_df(df, r, lbls, facets, qids, na_syns):
    year=r['year']
    logger.bind(year=year)
    logger.info('filtering, applying varlabels, munging')
    #lbls = {k:v for k,v in lbls.items()} ## if k in delayed(df.columns)}
    # get mapping into table for each facet
    facets = {r[k]:k for k in facets}
    ndf = (df.pipe(lambda xdf: filter_columns(xdf, facets, qids))
           .reset_index(drop=True)
           .apply(lambda x: eager_convert_categorical(x, lbls))
           .rename(index=str, columns=facets)
           .pipe(curry(find_na_synonyms)(na_syns))
           .pipe(lambda xf: xf.rename(index=str, columns={x: undash(x) for x in xf.columns}))
           .reset_index(drop=True)
           .assign(year = int(year) if type(year) == int else df[year].astype(int),
                   sitecode = df[r['sitecode']].apply(
                       SITECODE_TRANSLATORS['fips']).astype('category'),
                   weight = df[r['weight']].astype(float),
                   strata = df[r['strata']].astype(int),
                   psu = df[r['psu']].astype(int))
           .reset_index(drop=True))
    logger.info('completed SAS df munging')
    logger.unbind('year')
    return ndf



