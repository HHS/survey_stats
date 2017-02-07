from survey_stats.meta import SurveyMetadata
from survey_stats.datasets import YRBSSDataset


meta = {}
dset = {}

#fetch the state.metadata from Socrata
meta['yrbss'] = SurveyMetadata.load_metadata('data/yrbss.yaml')

#load survey datasets
dset['yrbss'] = YRBSSDataset.load_dataset('data/yrbss.yaml')


#state as singleton pattern
