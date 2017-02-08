import os
import pandas as pd
import feather
import logging
import numpy as np
import yaml
import json
import threading
from collections import namedtuple
from functools import reduce
from itertools import chain
from cached_property import cached_property, threaded_cached_property
from survey_stats.feathers import has_feather, load_feather, save_feather
from survey_stats.pdutil import guard_nan, fill_none


class SurveyMetadata(namedtuple('Metadata', ['config', 'qnmeta', 'dash'])):

    @classmethod
    def load_metadata(cls, yml_f):
        config = None
        with open(yml_f, 'r') as fh:
            config = yaml.load(fh)['dash']

        pfx = config['id']
        (qn, df) = (load_feather('qnmeta'), load_feather('dash')) if \
            has_feather('qnmeta') and has_feather('dash') else \
            cls.load_rawmeta(config)
        logging.info(df.shape)
        logging.info(df.columns)
        qn = qn.set_index(config['qnkey'])
        return cls(config=config, qnmeta=qn, dash=df)

    @classmethod
    def load_rawmeta(cls, cfg):
        # load dash data
        logging.info('loading raw dash data')
        df = pd.read_csv(cfg['files'][0], compression='gzip')
        # TODO: deal with multiple files
        # lowercase col names
        logging.info('renaming columns')
        df.columns = df.columns.map(lambda x: x.lower())
        k = cfg['qnkey']  # get the question key
        # rename questions (TODO: cleanup)
        logging.info('cleaning up question ids')
        df[k] = df[k].apply(lambda k:
                            k.replace('H', 'qn') if
                            k[0] == 'H' else
                            k.lower())
        logging.info('renaming columns')
        # rename columns
        df = df.rename(columns=cfg['rename'])
        logging.info('extracting all useful columns')
        allchain = [k] + list(chain.from_iterable(
            map(lambda x: cfg[x],
                ['facets', 'strata', 'stats', 'metadata'])))
        df = df[allchain]
        logging.info('converting object-types to categories')
        for col in df.columns:
            if df[col].dtype == np.dtype('O'):
                df[col] = df[col].astype('category')

        logging.info(df.dtypes)
        logging.info('deduplicating question metadata and saving')
        qnm = df[[k] + cfg['metadata']].drop_duplicates()
        logging.info('extracting dash table and saving')
        pre = df[[k] + list(chain.from_iterable(map(lambda x: cfg[x],
                                                    ['facets', 'strata', 'stats'])))]
        save_feather('qnmeta', qnm)
        save_feather('dash', pre)
        return (qnm, pre)


    def fetch_dash(self, qn, response, vars, filt = {}, is_national=True, year=None):
        cols = (['mean_yes', 'ci_h_yes', 'ci_l_yes','sample_size'] if response
            else ['mean_no', 'ci_h_no', 'ci_l_no','sample_size'])
        s_vars = self.config['facets']
        df = self.dash
        df = df[df['questioncode'] == qn]
        if is_national:
            df = df[df['stratificationtype'] == 'National']
        else:
            df = df[df['stratificationtype'] == 'State']
            if 'sitecode' in filt.keys():
                df = df[df['sitecode'] == filt['sitecode']]
        if 'year' in filt.keys():
            df = df[df['year'].isin(map( int, filt['year']))]
        if year:
            df = df[df['year'] == year]
        for v in s_vars:
            if not v in vars and not v == 'year':
                logging.info(v)
                logging.info(df.shape)
                df = df[(df[v] == 'Total')]
        if not 'year' in vars:
            vars.append('year')
        if not 'sitecode' in vars:
            vars.append('sitecode')
        df = df[vars + cols]
        df.columns = vars + ['mean','ci_h','ci_l','count']
        df['q'] = qn
        df['q_resp'] = response
        return df.to_dict(orient='records')

    @threaded_cached_property
    def qnmeta_dict(self):
        return json.loads(self.qnmeta.to_json(orient='index'))
