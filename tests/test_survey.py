import pandas as pd
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
from survey_stats.survey import subset_survey

def test_subset_survey():
    load_data = robjects.r('''
        function(){
            data(api)
            dclus1 = svydesign(id=~dnum, weights=~pw, data=apiclus1, fpc=~fpc)
            return(dclus1)
        }
    ''')
    rdf = load_data()
    f = {'sch.wide':['Yes'],
         'comp.imp':['Yes']}
    subdf = subset_survey(rdf, f)
    # test coment
    fetch_strata_dim = robjects.r('''
        function(s){
            return(dim(s$strata)[1])
        }
    ''')
    ssdim = pandas2ri.ri2py(fetch_strata_dim(subdf))
    assert ssdim == 133
    assert 1 == 1

