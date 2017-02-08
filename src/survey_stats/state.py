from survey_stats import log
from survey_stats.meta import SurveyMetadata
from survey_stats.datasets import YRBSSDataset
import logging

meta = {}
dset = {}

#fetch the state.metadata from Socrata
meta['yrbss'] = SurveyMetadata.load_metadata('data/yrbss.yaml')

#load survey datasets
dset['yrbss'] = YRBSSDataset.load_dataset('data/yrbss.yaml')

#state as singleton pattern
