import pandas as pd
import numpy as np
import asteval
import yaml
import sys
from cytoolz.curried import map, filter, curry
from cytoolz.functoolz import pipe, thread_first, thread_last, do
import dask
from dask import dataframe as dd
from dask.distributed import Executor
from dask import delayed
from dask.cache import Cache
from survey_stats import log
from survey_stats.etl import download as dl

logger = log.getLogger(__name__)

MAX_SOCRATA_FETCH=2**32


def doif(signal_arg, fn):
    if not signal_arg:
        return lambda x: x
    else:
        return curry(fn)(signal_arg)


def apply_fn2vals(fns, df):
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


def unstack_facets(df, unstack):
    logger.info('unstacking facet columns', unstack=unstack)
    for k,v in unstack.items():
        fcts = set(list(df[k]))
        logger.info('bagged distinct', f=fcts.compute())
        for c in fcts:
            df[c] = 'Total'
            df[c][df[k] == c] = df[v][df[k] == c]
            logger.info('unstacked facet column', col=c,
                        facets=df[c].value_counts(dropna=False).to_dict())
    logger.info('unstacking facet columns', cols=df.columns, unstack=unstack)
    return df


def fold_stats_cols(df, folds):
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


def munge_socrata_df(mapcols, mapvals, apply_fn, c_filter, df):
    return (df.pipe(doif(mapcols,
                        lambda m, df: df.rename(index=str, columns=m)))
            .pipe(doif(mapvals,
                       lambda m, df: df.replace(m)))
            .pipe(doif(apply_fn, apply_fn2vals))
            .pipe(doif(c_filter,
                       lambda cols, df: df[cols]))
            .pipe(delayed(coerce_dtypes)))


def fetch_socrata_stats(soda_api, mapcols, mapvals, apply_fn,
                        c_filter, unstack, fold_stats, qn_meta):
    df = thread_last(soda_api,
                     map(lambda u: u+'?'),
                     map(delayed(
                         dl.request_from_socrata_url)),
                     map(delayed(
                         lambda r: pd.DataFrame(r.json()))),
                     map(curry(munge_socrata_df)(mapcols, mapvals,
                                                 apply_fn, c_filter)),
                     delayed(pd.concat),
                     lambda x: x.compute(),
                     doif(unstack, unstack_facets),
                     doif(fold_stats, fold_stats_cols)
          )
    return df


def get_socrata_config(yaml_f):
    y = None
    with open(yaml_f) as fh:
        y = yaml.load(fh)
    return y['socrata']


def get_qids_by_year(yaml_f):
    y = get_socrata_config(yaml_f)
    mapcols = y['mapcols']
    revmap = {v:k for k,v in mapcols.items()}
    url = '{api_url}?' + \
            '$select=year,{qnkey},count(year)' + \
            '&$group=year,{qnkey}' + \
            '&$order={qnkey},year'
    qid = revmap['qid']
    df = thread_last(y['soda_api'],
                     map(lambda x: url.format(api_url=x, qnkey=qid)),
                     map(dl.df_from_socrata_url),
                     pd.concat)
    df.to_csv(sys.stdout)


def get_questions_socrata(yaml_f):
    revmap = {v: k for k, v in mapcols.items()}
    url = '{api_url}?' + \
            '$select={cols},count(year)' + \
            '&$group={cols}' + \
            '&$order={ocols}'

    qncols=','.join([revmap[k] for k in QNCOLS])
    ocols =','.join([revmap[k] for k in ['qid','year']])

    res = thread_last(y['soda_api'],
                      map(lambda x: url.format(api_url=x, cols=qncols, ocols=ocols)),
                      map(dl.df_from_socrata_url),
                      pd.concat)
    sl_res =[]
    sl_res = res[['facet', 'facet_description',
        'facet_level', 'facet_level_value']].drop_duplicates()
    sl_res = {f[0]: {
        'facet':f[0],
        'facet_description': f[1]['facet_description'].get_values()[0],
        'levels': dict(list(f[1][['facet_level','facet_level_value']].to_records(index=False)))
        } for f in sl_res.groupby('facet')}

    qn_res = res[['questionid', 'topic', 'subtopic', 'question', 'response']].groupby('questionid').agg({
        'topic': lambda x: x.head(1).get_values()[0],
        'subtopic': lambda x: x.get_values()[0],
        'question': lambda x: x.get_values()[0],
        'response': lambda x: list(x.drop_duplicates())
    })
    qn_res['class'] = qn_res['topic']
    qn_res['topic'] = qn_res['subtopic']
    del qn_res['subtopic']
    qn_res = qn_res.to_dict(orient='index')
    return qn_res

if __name__ == "__main__":
    get_qids_by_year('config/data/brfss_pre2011.yaml')
    #get_qids_by_year('config/data/yrbss.yaml')
