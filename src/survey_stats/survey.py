import pandas as pd
import rpy2
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

pandas2ri.activate()
rsvy = importr('survey')
rbase = importr('base')

class Survey(object):
    def __init__(self, data, survey_vars):
        self.df = data
        self.vars = survey_vars
        print(rbase.dim(self.df))
        print(data.shape)
