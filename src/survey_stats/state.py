from survey_stats import log
from survey_stats.datasets import SurveyDataset
import logging

meta = {}
dset = {}

#load survey datasets
dset['brfss'] = SurveyDataset.load_dataset('config/data/brfss.yaml')
dset['prams'] = SurveyDataset.load_dataset('config/data/prams.yaml')
dset['yrbss'] = SurveyDataset.load_dataset('config/data/yrbss.yaml')

#fetch the state.metadata from Socrata
'''
meta['brfss'] = SurveyMetadata.load_metadata('data/brfss.yaml')
meta['prams'] = SurveyMetadata.load_metadata('data/prams.yaml')
meta['yrbss'] = SurveyMetadata.load_metadata('data/yrbss.yaml')
'''
#state as singleton pattern
