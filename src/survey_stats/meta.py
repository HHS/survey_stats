import os
import pandas as pd
import feather
import logging
import numpy as np
import yaml
from collections import namedtuple
from functools import reduce
from itertools import chain
from survey_stats.cache import rcache
from survey_stats.feathers import has_feather, load_feather, save_feather

class SurveyMetadata(namedtuple('Metadata', ['config','qnmeta', 'precomp'])):
    __slots__ = ()


    @classmethod
    def load_metadata(cls, yml_f):
        config = None
        with open(yml_f, 'r') as fh:
            config = yaml.load(fh)['dash']
        pfx = config['id']
        (qn,df) = (load_feather('qnmeta'), load_feather('precomp')) if \
                has_feather('qnmeta') and has_feather('precomp') else \
                cls.load_rawmeta(config)
        return cls(config=config, qnmeta=qn, precomp=df)


    @classmethod
    def load_rawmeta(cls, cfg):
        # load dash data
        logging.info('loading raw dash data')
        df = pd.read_csv(cfg['files'][0], compression='gzip')
        #TODO: deal with multiple files
        #lowercase col names
        logging.info('renaming columns')
        df.columns = df.columns.map(lambda x: x.lower())
        k = cfg['qnkey'] #get the question key
        #rename questions (TODO: cleanup)
        logging.info('cleaning up question ids')
        df[k] = df[k].apply( lambda k:
                            k.replace('H','qn') if
                            k[0]=='H' else
                            k.lower())
        logging.info('renaming columns')
        #rename columns
        df = df.rename(columns=cfg['rename'])
        logging.info('extracting all useful columns')
        allchain = [k] + list(chain.from_iterable(
                map(lambda x: cfg[x],
                    ['facets','strata','stats','metadata'])))
        df = df[allchain]
        logging.info('converting object-types to categories')
        for col in df.columns:
            if df[col].dtype == np.dtype('O'):
                df[col] = df[col].astype('category')
        logging.info(df.dtypes)
        logging.info('deduplicating question metadata and saving')
        qnm = df[ [k]+cfg['metadata'] ].drop_duplicates().set_index(k)
        logging.info('extracting precomputed table and saving')
        pre = df[[k] + list(chain.from_iterable(map(lambda x: cfg[x],
                                       ['facets','strata','stats'] )))]
        save_feather('qnmeta', qnm)
        save_feather('precomp', pre)
        return (qnm, pre)

    @property
    def qnmeta_dict(self):
        return self.qnmeta.to_dict(orient='index')
