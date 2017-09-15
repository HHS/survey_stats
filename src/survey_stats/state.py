from survey_stats.datasets import SurveyDataset
from survey_stats import log
import os
import blaze as bz
import sqlalchemy as sa

lgr = log.getLogger(__name__)

meta = {}
dset = {}


def initialize(dbc, cache, init_des=False):
    lgr.info('was summoned into being, loading up some data', dbc=dbc, cache=cache)
    dset['brfss'] = SurveyDataset.load_dataset('config/data/brfss.yaml', dbc, cache, init_des)
    dset['yrbss'] = SurveyDataset.load_dataset('config/data/yrbss.yaml', dbc, cache, init_des)
