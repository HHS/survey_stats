import os
import pandas as pd
import feather
import logging
import numpy as np
import yaml
import ujson as json
import threading
from collections import namedtuple
from functools import reduce
from itertools import chain
from cached_property import cached_property, threaded_cached_property
from survey_stats.feathers import has_feather, load_feather, save_feather
from survey_stats.pdutil import guard_nan, fill_none
from survey_stats.log import logger
from survey_stats.error import SSEmptyFilterError, SSInvalidUsage

class SurveyMetadata(namedtuple('Metadata', ['config', 'qnmeta', 'dash'])):

    @classmethod
    def load_metadata(cls, yml_f):
        config = None
        with open(yml_f, 'r') as fh:
            config = yaml.load(fh)['dash']
        pfx = config['id']
        logger.info(pfx)
        (qn, df) = (load_feather(pfx+'.qnmeta'), load_feather(pfx+'.dash')) if \
                has_feather(pfx+'.qnmeta') and has_feather(pfx+'.dash') else \
                cls.load_rawmeta(config)
        logger.info(df.shape)
        logger.info(df.columns)
        qn = qn.set_index(config['qnkey'])
        return cls(config=config, qnmeta=qn, dash=df)

    @classmethod
    def load_rawmeta(cls, cfg):
        # load dash data
        logger.info('loading raw dash data')
        logger.info(cfg['files'])
        #df = pd.read_csv(cfg['files'][0], compression='gzip')
        df = pd.concat([pd.read_csv(f, index_col=None, header=0,
                                    compression='gzip')
                      for f in cfg['files']])
        # TODO: deal with multiple files
        # lowercase col names
        logger.info('renaming columns')
        df.columns = df.columns.map(lambda x: x.lower())
        qnkey = cfg['qnkey']  # get the question key
        # rename questions (TODO: cleanup)
        qpfx = cfg['qnpfx']
        logger.info('cleaning up question ids')
        df[qnkey] = df[qnkey].apply(lambda k:
                            k.replace(qpfx, 'qn') if
                            k.startswith(qpfx) else
                            k.lower())
        logger.info('renaming columns')
        # rename columns
        logger.info(cfg)
        #logger.info(cfg['response'])
        df = df.rename(columns=cfg['rename'])
        logger.info('extracting all useful columns')
        allchain = [qnkey] + list(chain.from_iterable(
            map(lambda x: cfg[x],
                ['facets', 'strata', 'stats', 'metadata', 'selectors'])))
        if 'fold_stats' in cfg:
            allchain = allchain  + cfg['fold_stats']['y'] + cfg['fold_stats']['n']

        allchain = allchain + cfg['response']
        allchain = set(df.columns).intersection(allchain)
        allchain = list(allchain)
        df = df[allchain]
        if 'remap' in cfg.keys():
            df.replace(cfg['remap'], inplace=True)
        try:
            df[cfg['response']] = df[cfg['response']].fillna('NA')
        except:
            pass
        if 'selectors' in cfg.keys():
            for s in cfg['selectors']:
                df[s].fillna('NA', inplace=True)

        if 'unstack' in cfg.keys():
            unstack = cfg['unstack']
            for k,v in unstack.items():
                catfacets = list(df[k].drop_duplicates())
                for c in catfacets:
                    df[c] = 'Total'
                    df[c][df[k] == c] = df[v][df[k] == c]
                    logger.info(df.shape)
                    logger.info(df[c].value_counts())
                cfg['facets'] = cfg['facets'] + catfacets

        logger.info(df.columns)
        logger.info('converting object-types to categories')
        for col in df.columns:
            if df[col].dtype == np.dtype('O'):
                df[col] = df[col].astype('category')
        logger.info(df.columns)
        if 'fold_stats' in cfg:
            logger.info(df.shape)
            cols = list(df.columns)
            yes_cols = cfg['fold_stats']['y']
            no_cols = cfg['fold_stats']['n']
            fixed_cols = list( set(cols) - set(yes_cols + no_cols) )
            yes_df = df[ fixed_cols + yes_cols ]
            no_df = df[ fixed_cols + no_cols ]
            yes_df['response'] = True
            no_df['response'] = False
            no_df.columns = yes_df.columns
            df = pd.concat([yes_df, no_df])
            df.reset_index(drop=True, inplace=True)
            logger.info(df.columns)
            logger.info(df.shape)
        logger.info('deduplicating question metadata and saving')
        logger.info('extracting dash table and saving')
        qnm = df[[qnkey] + cfg['metadata'] + cfg['response'] + cfg['selectors']].drop_duplicates()
        pre = [qnkey] + cfg['response'] + list(chain.from_iterable(map(lambda x: cfg[x],
                                                    ['facets', 'strata', 'stats'])))
        pre = set(df.columns).intersection(pre)
        pre = list(pre)
        pre = df[pre]
        # logger.info('pivoting facet and facet_level values')
        # facets_df = pre[['facet', 'facet_level']].drop_duplicates()
        # pre.drop(['facet', 'facet_level'], axis=1, inplace=True)
        # facets_df = facets_df.pivot(columns='facet', values='facet_level')
        # pre = pd.merge(pre, facets_df, left_index=True, right_index=True, how='left')
        pfx = cfg['id']
        save_feather(pfx+'.qnmeta', qnm)
        save_feather(pfx+'.dash', pre)
        return (qnm, pre)


    def fetch_dash(self, qn, response, vars, filt = {}):
        cols = self.config['stats']
        s_vars = self.config['facets']
        df = self.dash
        #TODO: consider the case where year is not mandatory in a precomp/Socrata DS
        if not 'year' in vars and not 'year' in filt.keys():
            raise ValueError('Must select a year in filter or in vars as '+
                                 'breakout for Socrata results.')
            #only available for indvividual years
        v_unk = [v for v in vars if v not in df.columns]
        if len(v_unk) > 0:
            raise ValueError('Encountered breakout variables not available '+
                             'in Socrata results: %s' % ','.join(v_unk))
        '''if not is_national and not 'sitecode' in vars:
            return [] #only available for individual states
        '''
        logger.info("columns")
        logger.info(df.columns)
        k = self.config['qnkey']  # get the question key
        df = df[df[k] == qn]
        logger.info(s_vars)
        logger.info(df.shape)
        nat_sel = self.config['national_selector']
        if 'sitecode' in filt.keys() or 'sitecode' in vars:
            if 'sitecode' in filt.keys():
                v='sitecode'
                df = df[df[v].isin(filt[v])]
                logger.info("filter key v: %s with vals %s leaves: %s" % (v,
                                                                          str(filt[v]),
                                                                          str(df.shape)))
        else:
            for k,v in nat_sel.items():
                logger.info("is national so selecting k: %s, v: %s" % (k,v))
                df = df[df[k] == v]
                logger.info(df.shape)
        if 'year' in filt.keys():
            logger.info("filtering by year: %s" % str(filt['year']))
            df = df[df['year'].isin(map( int, filt['year']))]
            logger.info(df.shape)
        for v in s_vars:
            if not v in vars and not v == 'year' and not v in filt.keys() and v in df.columns:
                df = df[df[v].isin(['Total', 'None'])]
                logger.info("total out v: %s leaves: %s" % (v,str(df.shape)))
            if v in filt.keys() and not v == 'year' and v in df.columns:
                df = df[df[v].isin(filt[v])]
                logger.info("filter key v: %s with vals %s leaves: %s" % (v,
                                                                          str(filt[v]),
                                                                          str(df.shape)))
        if "response" in df.columns:
            cols += ['response']
        df = df[vars + cols]
        df['q'] = qn
        for k in self.config['stats']:
            if k.startswith('mean') or k.startswith('ci'):
                df[k] = df[k]/100.0
        #df['level'] = df.apply(lambda x: np.sum(x[vars] != "Total"),axis=1)
        return df.to_dict(orient='records')

    @threaded_cached_property
    def qnmeta_dict(self):
        return json.loads(self.qnmeta.to_json(orient='index'))
