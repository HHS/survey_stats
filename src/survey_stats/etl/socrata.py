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
        if not k in df.columns:
            logger.info('skipping absent column', k=k)
            continue
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


def fetch_socrata_stats(url, soc_cfg, facets):
    g = soc_cfg
    url = url + '?' if url.find('?') == -1 else url
    logger.info('loading SODA data', url=url)
    df = (dl.df_from_socrata_url(url)
          .pipe(lambda xf: xf.applymap(lambda x: (re.sub('\xa0', '', x)).strip() if type(x) == str else x))
          .pipe(lambda xf: xf.rename(index=str, columns={x: x.lower() for x in
                                                         xf.columns}))
          .pipe(lambda xf: xf if not g.mapcols else xf.rename(index=str,
                                                              columns=g.mapcols))
          .pipe(apply_fn2vals, fns=g.apply_fn)
          .pipe(lambda xf: xf if not g.mapvals else xf.replace(g.mapvals))
          .pipe(unstack_facets, unstack=g.unstack)
          .pipe(fold_stats_cols, folds=g.fold_stats))

    cols = g.c_filter + list(set(facets).intersection(df.columns))
    miss_facets = list(set(facets).difference(df.columns))
    logger.warn('missing facets after filtering socrata columns', f=miss_facets)
    df = (df.pipe(lambda xf: xf[cols])
          .pipe(coerce_dtypes))
    return df


def load_socrata_data(cfg, facets):
    dfs = [delayed(fetch_socrata_stats)(url=url, soc_cfg=cfg, facets=facets) for
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
                     curry(pd.concat)(ignore_index=True))
    df.to_csv(sys.stdout)


def summarize_column(df, k):
    res = (df[[k]].drop_duplicates()
                  .apply(lambda xf: xf.astype(str))
                  .assign(facet=k)
                  .rename(index=str, columns={k: 'facet_level'}))
    logger.info('summarized a facet', k=k, res=res)
    return res.reset_index(drop=True)


def get_metadata_socrata(soc_cfg, soc_df, facets):
    g = soc_cfg
    # pull out question -> response breakouts
    qns = soc_df[g.qn_meta].drop_duplicates().reset_index(drop=True)
    # since facets are questions as well
    # update the dict with response value from fc_res
    # overriding the original var (N.B.)
    yrvec = summarize_column(soc_df, 'year')
    stvec = summarize_column(soc_df, 'sitecode')
    in_facets = list(set(facets).intersection(soc_df.columns))
    miss_facets = list(set(facets).difference(soc_df.columns))
    logger.warn('missing facets in generating socrata metadata', f=miss_facets)
    logger.warn('generating summary columns for facets', f=in_facets)
    facs = None
    if 'facet' in soc_df.columns:
        facs = (pd.concat(
            [soc_df[['facet', 'facet_level']].drop_duplicates(), yrvec, stvec],
            axis=0, ignore_index=True).reset_index(drop=True)
        )
    else:
        summs = list(map(lambda k: summarize_column(soc_df, k), in_facets))
        facs = pd.concat(summs + [yrvec, stvec], 
                         axis=0, ignore_index=True).reset_index(drop=True)
        facs = facs[facs.facet_level != "Total"]
    logger.info('created qn and fac metadata',
                qn=qns.dtypes.to_dict(),
                fac=list(facs.facet.drop_duplicates()))
    return (qns.reset_index(drop=True), facs.reset_index(drop=True))


    
def get_metadata_socrata_denovo(soc_cfg):
    g = soc_cfg
    revmap = {v: k for k, v in g.mapcols.items()}
    url = '{api_url}?' + \
          '$select={cols}' + \
          '&$order={ocols}'
    meta_diff = set(g.qn_meta).difference(g.computed)
    meta_diff = list(meta_diff)
    qncols = ','.join([(revmap[k] if
                        k in revmap else k) for
                       k in meta_diff])

    ocols = ','.join([revmap['qid'], 'year'])

    logger.info('loading SODA meta data')
    res = thread_last(
        g.soda_api,
        map(lambda x: url.format(api_url=x, cols=qncols, ocols=ocols)),
        map(dl.df_from_socrata_url),
        curry(pd.concat)(ignore_index=True))
    '''
        lambda xf: xf.applymap(lambda x: (re.sub('\xa0', '', x)).strip()),
        lambda xf: xf.rename(index=str, columns={x: x.lower() for x in
                                                 xf.columns}),
        lambda xf: xf if not g.mapcols else xf.rename(index=str,
                                                      columns=g.mapcols),
        curry(apply_fn2vals)(fns=g.apply_fn),
        lambda xf: xf if not g.mapvals else xf.replace(g.mapvals),
        lambda xf: xf if not g.mapvals else 
            xf.applymap(lambda x: g.mapvals[x.lower().strip()] if 
                        x.lower().strip() in g.mapvals else x),
        lambda xf: xf[g.qn_meta])
    '''
    logger.info('finished transformations', res=res.head())
    # pull out question -> response breakouts
    qns = res[['qid', 'year', 'topic',  
              'subtopic', 'question', 'response']].drop_duplicates().reset_index(drop=True)
    # since facets are questions as well
    # update the dict with response value from fc_res
    # overriding the original var (N.B.)
    yrvec = (res[['year']]
             .drop_duplicates()
             .assign(facet='year')
             .rename(index=str, columns={'year': 'facet_level'}))
    stvec = (res[['sitecode']]
             .drop_duplicates()
             .assign(facet='sitecode')
             .rename(index=str, columns={'sitecode':'facet_level'}))
    facs = pd.concat( [res[['facet', 'facet_level']].drop_duplicates(),
                       yrvec, stvec], axis=0).reset_index(drop=True)
    logger.info('created qn and facs', qn=qns.head(), fac=facs.head())
    return (qns, facs)


if __name__ == "__main__":
    get_qids_by_year('config/data/brfss_pre2011.yaml')
    # get_qids_by_year('config/data/yrbss.yaml')
