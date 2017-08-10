import pandas as pd
import numpy as np
import asteval
from survey_stats import log

MAX_SOCRATA_FETCH=2**32

logger = log.getLogger()

def unstack_facets(df, unstack):
    if not unstack:
        return df
    logger.info('unstacking facet columns', shape=df.shape, unstack=unstack)
    for k,v in unstack.items():
        fcts = list(df[k].drop_duplicates())
        for c in fcts:
            df[c] = 'Total'
            df[c][df[k] == c] = df[v][df[k] == c]
            logger.info('unstacked facet column', col=c,
                        facets=df[c].value_counts(dropna=False).to_dict())
        del df[k]
        del df[v]
    logger.info('unstacking facet columns', shape=df.shape, cols=df.columns,
                unstack=unstack)
    return df


def fold_stats(df, folds):
    if not folds:
        return df
    logger.info('folding df stats', shape=df.shape, folds=folds,
                cols='|'.join(df.columns))
    cols = list(df.columns)
    yes_cols = folds['y']
    no_cols = folds['n']
    fixed_cols = list( set(cols) - set(yes_cols + no_cols) )
    yes_df = df[ fixed_cols + yes_cols ]
    no_df = df[ fixed_cols + no_cols ]
    yes_df['response'] = 'Yes'
    no_df['response'] = 'No'
    no_df.columns = yes_df.columns
    df = pd.concat([yes_df, no_df], ignore_index=True).reset_index(drop=True)
    logger.info('folded df stats', shape=df.shape, folds=folds,
                cols='|'.join(df.columns))
    return df


def apply_fn2vals(df, fns):
    if not fns:
        return df
    evalr = asteval.Interpreter()
    for k,v in fns:
        logger.info('transforming col w/ apply_fn', col=k,
                    fn=v.replace('\n','\\n'))
        map_fn = evalr(v)
        df[k] = df[k].map(map_fn)
    return df


def coerce_dtypes(df):
    for col in df.columns:
        if col in ['mean','se','ci_u','ci_l']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[col].dtype == np.dtype('O'):
            df[col] = df[col].astype('category')
    logger.info('coerced columns to appropriate types',
                df.dtypes.to_dict())
    return df


def process_socrata_url(base_url, rename, remap, apply_fn, c_filter, unstack, fold_stats):
    url = '%s?$limit=%d' % (base_url, MAX_SOCRATA_FETCH)
    logger.info('loading SODA data', url=url)
    df = (pd.read_json(url)
          .pipe(lambda xf: xf.rename(index=str, columns={ x: x.lower() for x in
                                                         xf.columns }))
          .pipe(lambda xf: xf if not rename else xf.rename(index=str,
                                                           columns=rename))
          .pipe(lambda xf: xf if not remap else xf.replace(remap))
          .pipe(apply_fn2vals, fns=apply_fn)
          .pipe(lambda xf: xf if not c_filter else xf[c_filter])
          .assign(response=lambda x: x.response.fillna('NA'),
                  facet=lambda x: x.facet.fillna('NA'),
                  facet_level=lambda x: x.facet_level.fillna('NA'))
          .pipe(coerce_dtypes)
          .pipe(unstack_facets, unstack=unstack)
          .pipe(fold_stats, folds=fold_stats))
    return df

