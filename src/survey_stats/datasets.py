import os
import yaml
import ujson as json
import rpy2
from rpy2 import robjects
from rpy2.robjects.packages import importr
from collections import namedtuple

from survey_stats.log import logger
from survey_stats.survey import AnnotatedSurvey
from survey_stats.feathers import has_feather, load_feather

rfther = importr('feather', on_conflict='warn')
rutils = importr('utils')
rbase = importr('base')

cache_dir = os.path.join(os.getcwd(), 'cache')


class SurveyDataset(namedtuple('Dataset', ['config', 'surveys'])):
    __slots__ = ()

    @classmethod
    def load_dataset(cls, yml_f):
        config = None
        with open(yml_f, 'r') as fh:
            config = yaml.load(fh)['surveys']
        if not config:
            return cls(config=None, surveys=None)
        svys = {}
        for k, v in config.items():
            svys[k] = cls.fetch_or_load_dataset(k, v['spss'], v['data'])

        return cls(config=config, surveys=svys)

    def fetch_or_load_dataset(id, spss_f, data_f):
        f = os.path.join(cache_dir, '%s.feather' % id)
        ret = None
        rdf = None
        try:
            rdf = rfther.read_feather(f)
            ret = AnnotatedSurvey.from_rdf(spss_f, rdf)
            logger.info('loaded survey data from feather cache: %s' % f)
        except:
            logger.info('could not find feather cache, loading raw data')
            ret = AnnotatedSurvey.load_cdc_survey(spss_f, data_f)
            logger.info('saving data to feather cache: %s' % f)
            rfther.write_feather(ret.rdf, f)

        rbase.gc()
        return ret


class YRBSSDataset(SurveyDataset):
    __slots__ = ()

    def fetch_survey(self, combined=True, national=True, year=None):
        pred = (lambda v: v['is_combined'] == combined and
                (v['year'] == year if year else True))
        if not self.config:
            return None
        return next(( self.surveys[k] for k, v in self.config.items() if pred(v)), None)

    def fetch_config(self, national=True, year=None):
        combined = not year # if year is present, get ind year, else combined
        pred = (lambda v: v['is_combined'] == combined and
                (v['year'] == year if year else True))
        if not self.config:
            return None
        return next(((k, v) for k, v in self.config.items() if pred(v)), None)


    @property
    def survey_years(self):
        return set(sorted([int(v['year']) for v in self.config.values()]))
