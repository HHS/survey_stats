import pandas as pd
import numpy as np
import asteval
from survey_stats import log

MAX_SOCRATA_FETCH=2**32

logger = log.getLogger(__name__)

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


def process_socrata_url(yaml_f):
    with open(yaml_f) as fh:
        y = yaml.load(fh)
    url = '%s?$limit=%d' % (soda_api[0], MAX_SOCRATA_FETCH)
    logger.info('loading SODA data', url=url)
    df = (pd.read_json(url)
          .pipe(lambda xf: xf.rename(index=str, columns={ x: x.lower() for x in
                                                         xf.columns }))
          .pipe(lambda xf: xf if not mapcols else xf.rename(index=str,
                                                           columns=mapcols))
          .pipe(lambda xf: xf if not mapvals else xf.replace(mapvals))
          .pipe(apply_fn2vals, fns=apply_fn)
          .pipe(lambda xf: xf if not c_filter else xf[c_filter])
          .assign(response=lambda x: x.response.fillna('NA'),
                  facet=lambda x: x.facet.fillna('NA'),
                  facet_level=lambda x: x.facet_level.fillna('NA'))
          .pipe(coerce_dtypes)
          .pipe(unstack_facets, unstack=unstack)
          .pipe(fold_stats_cols, folds=fold_stats)
          .pipe(lambda xf: xf.replace(
              {col:{'NA':np.nan} for col in xf.columns}))
        )
    return df


def get_qids_by_year(yaml_f):
    url = '{api_url}?$limit={limit}&' + \
            '$select=year,{qnkey},count(year)' + \
            '&$group=year,{qnkey}' + \
            '&$order={qnkey},year'
    url = url.format(api_url=soda_api, limit=MAX_SOCRATA_FETCH, qnkey=qnkey)
    df = pd.read_json(url)
    pass


def get_questions_socrata(yaml_f):
    revmap = {v: k for k, v in mapcols.items()}
    url = '{api_url}?$limit={limit}&' + \
            '$select={cols},count(year)' + \
            '&$group={cols}' + \
            '&$order={ocols}'
    url = url.format(api_url=soda_api,
                     limit=MAX_SOCRATA_FETCH,
                     cols=','.join([revmap[k] for k in QNCOLS]),
                     ocols =','.join([revmap[k] for k in ['qid','year']]))
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
