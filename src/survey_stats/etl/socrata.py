import pandas as pd
import numpy as np
import asteval
import sys
from cytoolz.curried import map, curry
from cytoolz.functoolz import thread_last
from cytoolz.dicttoolz import assoc_in
from dask import delayed
import re
from survey_stats import log
from survey_stats.etl import download as dl
from survey_stats import pdutil

logger = log.getLogger(__name__)


def unstack_facets(df, unstack):
    if not unstack:
        return df
    logger.info('unstacking facet columns', shape=df.shape, unstack=unstack)
    for k, v in unstack.items():
        fcts = list(df[k].drop_duplicates())
        for c in fcts:
            df[c] = 'Total'
            df[c][df[k] == c] = df[v][df[k] == c]
            logger.info('unstacked facet column', col=c,
                        facets=df[c].value_counts(dropna=False).to_dict())
    logger.info('unstacking facet columns', shape=df.shape, cols=df.columns,
                unstack=unstack)
    return df


def fold_stats_cols(df, folds):
    if not folds:
        return df
    logger.info('folding df stats', shape=df.shape, folds=folds,
                cols='|'.join(df.columns))
    cols = list(df.columns)
    yes_cols = folds['y']
    no_cols = folds['n']
    fixed_cols = list(set(cols) - set(yes_cols + no_cols))
    yes_df = df[fixed_cols + yes_cols]
    no_df = df[fixed_cols + no_cols]
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
    evalr.symtable['pdutil'] = pdutil
    for k, v in fns.items():
        logger.info('transforming col w/ apply_fn', col=k,
                    fn=v.replace('\n', '\\n'))
        map_fn = evalr(v)
        df[k] = df[k].map(map_fn)
    return df


def coerce_dtypes(df):
    for col in df.columns:
        if col in ['mean', 'se', 'ci_u', 'ci_l']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[col].dtype == np.dtype('O'):
            df[col] = df[col].astype('category')
    logger.info('coerced columns to appropriate types',
                df.dtypes.to_dict())
    return df


def fetch_socrata_stats(url, soc_cfg):
    g = soc_cfg
    logger.info('loading SODA data', url=url)
    df = (dl.df_from_socrata_url(url+'?')
          .pipe(lambda xf: xf.applymap(lambda x: (re.sub('\xa0', '', x)).strip() if type(x) == str else x))
          .pipe(lambda xf: xf.rename(index=str, columns={x: x.lower() for x in
                                                         xf.columns}))
          .pipe(lambda xf: xf if not g.mapcols else xf.rename(index=str,
                                                              columns=g.mapcols))
          .pipe(apply_fn2vals, fns=g.apply_fn)
          .pipe(lambda xf: xf if not g.mapvals else xf.replace(g.mapvals))
          .pipe(lambda xf: xf if not g.c_filter else xf[g.c_filter])
          .assign(response=lambda x: x.response,
                  facet=lambda x: x.facet,
                  facet_level=lambda x: x.facet_level)
          .pipe(coerce_dtypes)
          .pipe(unstack_facets, unstack=g.unstack)
          .pipe(fold_stats_cols, folds=g.fold_stats))
    return df


def load_socrata_data(cfg, client=None):
    dfs = [delayed(fetch_socrata_stats)(url=url, soc_cfg=cfg) for
           url in cfg.soda_api]
    dfs = delayed(pd.concat)(dfs, ignore_index=True)
    dfs = dfs.compute()
    return dfs


def get_qids_by_year(soc_cfg):
    g = soc_cfg
    revmap = {v: k for k, v in g.mapcols.items()}
    url = '{api_url}?' + \
          '$select=year,{qnkey},count(year)' + \
          '&$group=year,{qnkey}' + \
          '&$order={qnkey},year'
    qid = revmap['qid']
    df = thread_last(g.soda_api,
                     map(lambda x: url.format(api_url=x, qnkey=qid)),
                     map(dl.df_from_socrata_url),
                     pd.concat)
    df.to_csv(sys.stdout)


def get_metadata_socrata(soc_cfg):
    g = soc_cfg
    revmap = {v: k for k, v in g.mapcols.items()}
    url = '{api_url}?' + \
          '$select={cols}' + \
          '&$order={ocols}'
    qncols = ','.join([(revmap[k] if
                        k in revmap else k) for
                       k in g.qn_meta])

    ocols = ','.join([revmap['qid'], 'year'])

    logger.info('loading SODA meta data')
    res = thread_last(
        g.soda_api,
        map(lambda x: url.format(api_url=x, cols=qncols, ocols=ocols)),
        map(dl.df_from_socrata_url),
        pd.concat,
        lambda xf: xf.applymap(lambda x: (re.sub('\xa0', '', x)).strip()),
        lambda xf: xf.rename(index=str, columns={x: x.lower() for x in
                                                 xf.columns}),
        lambda xf: xf if not g.mapcols else xf.rename(index=str,
                                                      columns=g.mapcols),
        curry(apply_fn2vals)(fns=g.apply_fn),
        lambda xf: xf if not g.mapvals else xf.replace(g.mapvals),
        lambda xf: xf if not g.mapvals else xf.applymap(lambda x: g.mapvals[x.lower().strip()] if x.lower().strip() in g.mapvals else x),
        lambda xf: xf if not g.qn_meta else xf[g.qn_meta],
        lambda xf: xf.assign(response=lambda x: x.response,
                             facet=lambda x: x.facet,
                             facet_level=lambda x: x.facet_level))
    logger.info('finished transformations', res=res.head())
    # pull out question -> response breakouts
    qns = (res.groupby(['qid', 'year', 'sitecode'])
           .agg({'topic': lambda x: x.get_values()[0],
                 'subtopic': lambda x: x.get_values()[0],
                 'question': lambda x: x.get_values()[0],
                 'response': lambda x: list(x.drop_duplicates())
                 })
           .reset_index()
           .to_dict(orient='records'))
    fct = (res[['facet', 'facet_level']]
           .groupby(['facet'])
           .agg({'facet_level': lambda x: list(x.drop_duplicates())})
           .rename(index=str, columns={'facet_level': 'response'})
           .to_dict())
    # since facets are questions as well
    # update the dict with response value from fc_res
    # overriding the original var (N.B.)
    qns = map(lambda d:
              assoc_in(d, ['response'],
                       fct[d['qid']] if d['qid'] in
                       fct else d['response']),
              qns)
    return list(qns)


if __name__ == "__main__":
    get_qids_by_year('config/data/brfss_pre2011.yaml')
    # get_qids_by_year('config/data/yrbss.yaml')
