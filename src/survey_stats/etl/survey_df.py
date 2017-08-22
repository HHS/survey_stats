import us
import pandas as pd
import numpy as np
from cytoolz.itertoolz import mapcat
from cytoolz.functoolz import thread_last
from cytoolz.curried import map, filter, curry
from survey_stats import log
from survey_stats import pdutil

import dask
from dask import distributed as dd
from dask import delayed
from dask import bag
from dask.distributed import Client

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
    return c


def eager_convert_categorical(s, lbls):
    if not s.name in lbls.keys():
        return s
    try:
        c = (pd.to_numeric(s.fillna(-1), downcast='integer')
             .astype('category'))
        c = c.cat.rename_categories(
            [lbls[s.name][k] for k in sorted(c.unique())])
        c = (c.cat.set_categories([
                lbls[s.name][k] for k in
                sorted(lbls[s.name].keys())
             ]).astype('category'))
        return c
    except KeyError:
        return s
    except ValueError as e:
        logger.info('found value err', err=e, c=str(c.value_counts(dropna=False)),
                    c_desc=c.describe())
        return force_convert_categorical(s, lbls)


def filter_columns(df, facets, qids):
    set_union = lambda x,y: y.union(x)
    cols = thread_last(set(qids),
                       (set_union, facets.keys()),
                       lambda x: x.intersection(df.columns),
                       list,
                       sorted)
    ndf = df[cols]
    logger.info("filtered df columns", qids=','.join(qids),
                facets=','.join(facets.keys()),
                filtered=','.join(cols),
                missing=set(cols).difference(df.columns),
                ncols=len(cols), old_shape=df.shape, new_shape=ndf.shape)
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
    logger.info('filtering, applying varlabels, munging')
    ''', cols=df.columns,
                shape=df.shape, dups=pdutil.duplicated_varnames(df))
    '''
    lbls = {k:v for k,v in lbls.items()} ## if k in delayed(df.columns)}
    facets = {r[k]:k for k in facets}
    year=r['year']
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
    ''',
                summary=ndf.dtypes.value_counts(dropna=False).to_dict(),
                shape=ndf.shape, dups=pdutil.duplicated_varnames(df),
                years=ndf['year'].value_counts().to_dict(),
                sitecodes=ndf['sitecode'].value_counts().to_dict(),
                strata=ndf['strata'].describe().to_dict())'''
    return ndf



