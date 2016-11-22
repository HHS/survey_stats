import sys
import pandas as pd
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.functions import SignatureTranslatedFunction
from rpy2.robjects import IntVector, FactorVector, ListVector, StrVector
from rpy2.robjects import Formula
import pandas.rpy.common as com
pandas2ri.activate()

sys.path.append("/Users/ajish/MEGA/dev/semanticbits/owh/survey_stats/src/survey_stats")

import parsers.cdc_yrbs as cdc
import survey

rsvy = importr('survey')
rbase = importr('base')

spss_file = "data/YRBS_2015_SPSS_Syntax.sps"
dat_file = "data/yrbs2015.dat"

cols = cdc.parse_fwfcols_spss(spss_file)
vars = cdc.parse_surveyvars_spss(spss_file)
print(cols)
print(vars)
df = pd.read_fwf(dat_file, colspecs=list(cols.values()),
                 names=list(cols.keys()))
#s = survey.Survey(df, vars)

#rdf = pandas2ri.py2ri_pandasdataframe(df)


rdf = com.convert_to_r_dataframe(df)
print(rbase.colnames(rdf))

for q, v in vars.items():
    if len(v['responses']) > 0:
        print q
        (codes, cats) = zip(*v['responses'])
        idx = rdf.colnames.index(q)
        fac = rbase.as_integer(rdf[idx])
        fac = rbase.factor(fac, labels=list(cats))
        print(rbase.summary(fac))
        rdf[idx] = fac
    elif q.startswith('qn'):
        print q
        idx = rdf.colnames.index(q)
        fac = rbase.as_integer(rdf[idx])
        fac = rbase.factor(fac, labels=['Yes','No'])
        print(rbase.summary(fac))
        rdf[idx] = fac

print(rbase.summary(rdf))

yrbsdes = rsvy.svydesign(id=Formula("~psu"), weight=Formula("~weight"),
                        strata=Formula("~stratum"), data=rdf, nest=True)


svymean_rmna = robjects.r('''
    function(x, design, na.rm, deff=FALSE, ...) {
      svymean(x, design, TRUE, deff, ...)
    }''')

svyciprop_yrbs = robjects.r('''
    function(formula, design, method="xlogit", level = 0.95,
             df=degf(design), ...) {
        svyciprop(formula, design, method, level, df, na.rm=TRUE, ...)
    }''')


helmet_ci = svyciprop_yrbs(Formula("~I(qn8==1)"), yrbsdes, na_rm=True,
                           method="xlogit")

helmet_mu = rsvy.svyby(Formula("~qn8"),
                       Formula("~q2 + raceeth"), yrbsdes,
                       svymean_rmna, keep_var=True, vartype="ci",
                       method="xlogit")
robjects.globalenv["yrbsdes"] = yrbsdes
robjects.globalenv["rdf"] = rdf
rbase.save( "yrbsdes", "rdf", file="loaded.RData")

print(helmet_mu)
print(helmet_ci)
#widths = list(map(lambda x: x[1]-x[0], list(cols.values())))
#print(widths)
#widths = [-16] + widths

#names = list(cols.keys())
#print(widths)
#print(names)
#print(dat_file)
#as_factor = robjects.r['as.factor']
#read_fwf = robjects.r['read.fwf']
#fwf_read = SignatureTranslatedFunction(read_fwf, init_prm_translate = {
#    'as_is': 'as.is',
#    'strip_white': 'strip.white',
#    'na_strings': 'na.strings',
#    'col_names': 'col.names'
#})

#rdat = fwf_read(dat_file, as_is=True, strip_white=True,
#                      na_strings='.', widths=widths, col_names=names)

#print(rbase.summary(rdat))
#print(rbase.dim(rdat))
