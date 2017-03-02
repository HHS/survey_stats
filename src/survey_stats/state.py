from survey_stats import log
from survey_stats.meta import SurveyMetadata
from survey_stats.datasets import YRBSSDataset
import logging

meta = {}
dset = {}

#load survey datasets
dset['prams'] = YRBSSDataset.load_dataset('data/prams.yaml')
dset['yrbss'] = YRBSSDataset.load_dataset('data/yrbss.yaml')

#fetch the state.metadata from Socrata
meta['prams'] = SurveyMetadata.load_metadata('data/prams.yaml')
meta['yrbss'] = SurveyMetadata.load_metadata('data/yrbss.yaml')

#state as singleton pattern
