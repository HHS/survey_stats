import sys
import pandas as pd
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.functions import SignatureTranslatedFunction

pandas2ri.activate()

sys.path.append("/Users/ajish/semanticbits/owh/survey_stats/src/survey_stats")

import parsers.cdc_yrbs as cdc
import survey

rsvy = importr('survey')
rbase = importr('base')

spss_file = "data/YRBS_2015_SPSS_Syntax.sps"
dat_file = "data/yrbs2015.dat"

cols = cdc.parse_fwfcols_spss(spss_file)
vars = cdc.parse_surveyvars_spss(dat_file)

#df = pd.read_fwf(dat_file, colspecs=list(cols.values()),
#                 names=list(cols.keys()))
#s = survey.Survey(df, vars)

widths = list(map(lambda x: x[1]-x[0], list(cols.values())))
print(widths)
#widths = [-16] + widths

names = list(cols.keys())
print(widths)
print(names)
print(dat_file)
as_factor = robjects.r['as.factor']
read_fwf = robjects.r['read.fwf']
fwf_read = SignatureTranslatedFunction(read_fwf, init_prm_translate = {
    'as_is': 'as.is',
    'strip_white': 'strip.white',
    'na_strings': 'na.strings',
    'col_names': 'col.names'
})

rdat = fwf_read(dat_file, as_is=True, strip_white=True,
                      na_strings='.', widths=widths, col_names=names)

print(rbase.summary(rdat))
print(rbase.dim(rdat))
