import us
import pandas as pd
import numpy as np
from cytoolz.itertoolz import mapcat
from cytoolz.functoolz import thread_last
from cytoolz.curried import map, filter

from survey_stats import log


logger = log.getLogger(__name__)


US_STATES_FIPS_INTS = thread_last(
    us.STATES_AND_TERRITORIES,
    map(lambda x: x.fips),
    filter(lambda x: x is not None),
    map(lambda x: int(x)),
    list
)

SITECODE_TRANSLATORS = {
    'fips': lambda x: (us.states.lookup('%.2d' % x).abbr if int(x) in US_STATES_FIPS_INTS else 'NA')
}

SVYDESIGN_COLS = ['sitecode', 'strata', 'psu', 'weight']

def force_convert_categorical(s, lbls):
    c = (pd.to_numeric(s.fillna(-1), downcast='integer')
         .replace(to_replace=lbls[s.name])
         .astype('category'))
    #logger.info('forced cat conversion', c=str(c.value_counts(dropna=False)),
    #            c_desc=str(c.describe()))
    return c


def eager_convert_categorical(s, lbls):
    if not s.name in lbls.keys():
        return s
    try:
        c = (pd.to_numeric(s.fillna(-1), downcast='integer')
             .astype('category'))
        #logger.info('eager conv - 1', summ=c.value_counts(dropna=False).to_dict(),
        #            labels=lbls[s.name])
        c = c.cat.rename_categories(
            [lbls[s.name][k] for k in sorted(c.unique())])
        #logger.info('eager conv - 2', summ=c.value_counts(dropna=False).to_dict(),
        #            keys=sorted(lbls[s.name].keys()))
        c = (c.cat.set_categories(
            [lbls[s.name][k] for k in sorted(lbls[s.name].keys())])
            .astype('category'))
        #logger.info('eager conv - 3', summ=c.value_counts(dropna=False).to_dict(),
        #            desc = str(c.describe()))
        return c
    except KeyError:
        return s
    except ValueError as e:
        logger.info('found value err', err=e, c=str(c.value_counts(dropna=False)),
                    c_desc=c.describe())
        return force_convert_categorical(s, lbls)


def filter_columns(df, r, facets, qids):
    set_union = lambda x,y: y.union(x)
    cols = thread_last(set(qids),
                       (set_union, map(lambda x: r[x], SVYDESIGN_COLS)),
                       (set_union, facets.keys()),
                       lambda x: x.intersection(df.columns),
                       list,
                       sorted)
    ndf = df[cols]
    logger.info("filtered df columns", qids=','.join(qids),
                facets=','.join(facets.keys()),
                fixed=','.join(map(lambda x: r[x], SVYDESIGN_COLS)),
                filtered=','.join(cols),
                missing=set(cols).difference(df.columns),
                ncols=len(cols), old_shape=df.shape, new_shape=ndf.shape)
    return ndf


def munge_df(df, lbls, facets, year, sitecode, weight, strata, psu):
    logger.info('filtering, applying varlabels, munging')
    ndf = (filter_columns(df, r, facets, qids)
           .apply(lambda x: eager_convert_categorical(x, lbls))
           .select_dtypes(include=['category'])
           .rename(index=str, columns=facets)
           .assign(year = int(year) if year.isnumeric else df[year].astype(int),
                   sitecode = df[sitecode].apply(
                        SITECODE_TRANSLATORS['fips']).astype('category'),
                   weight = df[weight].astype(float),
                   strata = df[strata].astype(int),
                   psu = df[psu].astype(int))
    )
    logger.info('completed SAS df munging',
                summary=ndf.dtypes.value_counts(dropna=False).to_dict(),
                shape=ndf.shape, dups=pdutil.duplicated_varnames(df))
    return ndf


def find_na_synonyms(df, na_syns):
    df = df.applymap(
        lambda x: np.nan if
        (x.lower() in na_syns if
            type(x) == str else
            False)
        else x)
    return df


def merge_multiyear_surveys(dfs, na_syns):
    logger.info('merging SAS dfs')
    undash_fn = lambda x: 'x' + x if x[0] == '_' else x
    dfs = (pd.concat(dfs, ignore_index=True)
           .pipe(lambda xf: find_na_synonyms(xf, na_syns))
           .apply(lambda x: x.astype('category') if
                 x.dtype.name in ['O','object'] else x)
           .pipe(lambda xf: xf.rename(index=str, columns={x:undash_fn(x) for x
                                                          in xf.columns})))
    logger.info('merged SAS dfs', shape=dfs.shape,
                 summary=dfs.dtypes.value_counts(dropna=False).to_dict())
