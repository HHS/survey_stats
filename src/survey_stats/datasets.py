import os
import logging
import yaml
import feather

import rpy2
from rpy2 import robjects
from rpy2.robjects.packages import importr
from collections import namedtuple
from survey import AnnotatedSurvey

#TODO: install from remote yaml
#import appdirs

rfther = importr('feather', on_conflict='warn')

cache_dir = os.path.join(os.getcwd(), 'cache')


class SurveyDataset(namedtuple('Dataset', ['config','surveys'])):
    __slots__ = ()


    @classmethod
    def load_dataset(cls, yml_f):
        config = None
        with open(yml_f, 'r') as fh:
            config = yaml.load(fh)['surveys']
            print(config)
        svys = {}
        for k,v in config.items():
            print(v)
            svys[k] = cls.fetch_or_load_dataset(k, v['spss'], v['data'])
        return cls(config=config, surveys=svys)

    def fetch_or_load_dataset(id, spss_f, data_f):
        f = os.path.join(cache_dir, '%s.feather' % id)
        ret = None
        rdf = None
        try:
            rdf = rfther.read_feather(f)
            ret = AnnotatedSurvey.from_rdf(spss_f, rdf)
            logging.info('loaded survey data from feather cache: %s' % f)
        except:
            logging.info('could not find feather cache, loading raw data')
            ret = AnnotatedSurvey.load_cdc_survey(spss_f, data_f)
            logging.info('saving data to feather cache: %s' % f)
            rfther.write_feather(ret.rdf, f)
        return ret


    def fetch_survey(self, combined=True, national=True, year=None):
        for k, v in self.config.items():
            print((combined, national, year, v))
            yr_pred = v['year'] == year if year else True
            if v['is_combined'] == combined and \
               v['is_national'] == national and \
               yr_pred:
                return self.surveys[k]
        return None



