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

sys.path.append('src/survey_stats')

import parsers.cdc_yrbs as cdc
import survey

from sanic import Sanic
from sanic.response import json

rsvy = importr('survey')
rbase = importr('base')

spss_file = 'data/YRBS_2015_SPSS_Syntax.sps'
dat_file = 'data/yrbs2015.dat'

svy_cols = cdc.parse_fwfcols_spss(spss_file)
svy_vars = cdc.parse_surveyvars_spss(spss_file)

df = pd.read_fwf(dat_file, colspecs=list(svy_cols.values()),
                 names=list(svy_cols.keys()))

rdf = com.convert_to_r_dataframe(df)


tobool_yrbs = robjects.r('''
    function(col) {
        as.logical( 2 - col)
    } ''')


for q, v in svy_vars.items():
    if len(v['responses']) > 0:
        (codes, cats) = zip(*v['responses'])
        idx = rdf.colnames.index(q)
        fac = rbase.as_integer(rdf[idx])
        fac = rbase.factor(fac, labels=list(cats))
        rdf[idx] = fac
    elif q.startswith('qn'):
        idx = rdf.colnames.index(q)
        fac = tobool_yrbs(rdf[idx])
        rdf[idx] = fac


yrbsdes = rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
                        strata=Formula('~stratum'), data=rdf, nest=True)


svyciprop_yrbs = robjects.r('''
    function(formula, design, method='xlogit', level = 0.95,
             df=degf(design), ...) {
        svyciprop(formula, design, method, level, df, na.rm=TRUE, ...)
    }''')

svybyci_yrbs = robjects.r('''
    function( formula, by, des, fn, ...) {
        svyby(formula, by, des, fn, keep_var=True, method='xlogit',
              vartype=c('se','ci'))
    }''')


'''sample calls
robjects.globalenv['yrbsdes'] = yrbsdes
robjects.globalenv['rdf'] = rdf
rbase.save('yrbsdes', 'rdf', file='save.RData')

ci = svyciprop_yrbs(Formula('~!qn8'), yrbsdes, na_rm=True,
                           method='xlogit')

byci = rsvy.svyby(Formula('~!qn8'), Formula('~q2 + raceeth'),
                  yrbsdes, rsvy.svyciprop, method='xlogit',
                  na_rm=True, vartype=StrVector(['se','ci']))

byct = rsvy.svyby(Formula('~!qn8'), Formula('~q2 + raceeth'),
                         yrbsdes, rsvy.unwtd_count, na_rm=True)

'''

def fetch_stats(des, qn, response=True, vars=[]):
    DECIMALS = {
        'mean': 4, 'se': 4, 'ci_l': 4, 'ci_u': 4, 'count':0
    }
    def fetch_stats_by(vars, qn_f, des):
        lvl_f = Formula('~%s' % ' + '.join(vars))
        ci = svybyci_yrbs(qn_f, lvl_f, des, svyciprop_yrbs)
        ct = rsvy.svyby(qn_f, lvl_f, des, rsvy.unwtd_count, na_rm=True)
        merged = pandas2ri.ri2py(rbase.merge(ci, ct))
        del merged['se']
        merged.columns = vars + ['mean', 'se', 'ci_l', 'ci_u', 'count']
        merged['level'] = len(vars)
        merged['q'] = qn
        merged['q_resp'] = response
        merged = merged.round(DECIMALS)
        return merged.apply(lambda r: r.to_dict(), axis=1)
    # create formula for selected question and risk profile
    # ex: ~qn8, ~!qn8
    qn_f = Formula('~%s%s' % ('' if response else '!', qn))
    total_ci = svyciprop_yrbs(qn_f, des, na_rm=True, method='xlogit')
    total_ct = rsvy.unwtd_count(qn_f, des, na_rm=True)
    #extract stats
    res = {'level': 0,
            'mean': rbase.as_numeric(total_ci)[0],
            'se': rsvy.SE(total_ci)[0],
            'ci_l': rbase.attr(total_ci,'ci')[0],
            'ci_u': rbase.attr(total_ci,'ci')[1],
            'count': rbase.as_numeric(total_ct)[0]}
    #round as appropriate
    res = {k: round(v, DECIMALS[k]) if k in DECIMALS else v for k,v in
           res.items()}
    #setup the result list
    res = [res]
    vstack = vars[:]
    while len(vstack) > 0:
        #get stats for each level of interactions in vars
        #using svyby to compute across combinations of loadings
        res.extend(fetch_stats_by(vstack, qn_f, des))
        vstack.pop()
    return res


fetch_stats(yrbsdes, 'qn8', True, ['q2', 'raceeth'])

app = Sanic(__name__)

@app.route("/national")
async def fetch_national(req):
    qn = req.args['q'][0]
    vars = [] if not 'v' in req.args else req.args['v'][0].split(',')
    resp = True if not 'r' in req.args else int(req.args['r'][0]) > 0
    #return json({ "parsed": True, "args": req.args, "url": req.url,
    #             "query_string": req.query_string })
    return json({
        "q": qn,
        "question": svy_vars[qn]['question'],
        "response": resp,
        "vars": vars,
        "var_levels": {v: svy_vars[v] for v in vars},
        "results": fetch_stats(yrbsdes, qn, resp, vars)
    })

app.run(host="0.0.0.0", port=7777, debug=True)

