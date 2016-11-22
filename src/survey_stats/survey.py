import pandas as pd
import rpy2
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import pandas.rpy.common as com
from rpy2.robjects.functions import SignatureTranslatedFunction
from rpy2.robjects import IntVector, Formula
import pandas.rpy.common as com
pandas2ri.activate()

rsvy = importr('survey')
rbase = importr('base')

class Survey(object):
    def __init__(self, data, survey_vars):
        self.df = com.convert_to_r_dataframe(data)
        self.vars = survey_vars
        print(rbase.summary(self.df))
        print(data.shape)
        yrbsdes = rsvy.svydesign(id=Formula("~psu"), weight=Formula("~weight"),
                                strata=Formula("~stratum"), data=rdf, nest=True)

