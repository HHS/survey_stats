from survey_stats.datasets import SurveyDataset
from survey_stats import log

lgr = log.getLogger(__name__)

dset = {}


def initialize(dbc, cache, init_des, use_feather, init_svy, init_soc):
    lgr.info('was summoned into being, loading up some data', dbc=dbc, cache=cache, use_feather=use_feather)
    dset['brfss'] = SurveyDataset.load_dataset('config/data/brfss.yaml', dbc, cache, init_des, use_feather, init_svy, init_soc)
    dset['brfss_pre2011'] = SurveyDataset.load_dataset('config/data/brfss_pre2011.yaml', dbc, cache, init_des, use_feather, init_svy, init_soc)
    dset['yrbss'] = SurveyDataset.load_dataset('config/data/yrbss.yaml', dbc, cache, init_des, use_feather, init_svy, init_soc)
    dset['prams'] = SurveyDataset.load_dataset('config/data/prams.yaml', dbc, cache, init_des, use_feather, init_svy, init_soc)
    dset['prams_p2011'] = SurveyDataset.load_dataset('config/data/prams_p2011.yaml', dbc, cache, init_des, use_feather, init_svy, init_soc)
