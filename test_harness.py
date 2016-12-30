from __future__ import print_function
import sys
import backtracepython as bt
import pandas as pd
import logging
from collections import namedtuple
from collections import OrderedDict
#from cachetools import cached, LRUCache
from threading import RLock
import gc
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.functions import SignatureTranslatedFunction
from rpy2.robjects import IntVector, FactorVector, ListVector, StrVector
from rpy2.robjects import Formula
import pandas.rpy.common as com

pandas2ri.activate()

bt.initialize(
  endpoint="https://rootedinsights.sp.backtrace.io:6098",
  token="768367df71e2be15321e851494b6dcc7152bf8f48fe5cc85a2deac80b94a31e9"
)

sys.path.append('src/survey_stats')

import parsers.cdc_yrbs as cdc
import survey

logging.basicConfig(level=logging.DEBUG)

rsvy = importr('survey')
rbase = importr('base')
rfunc = importr('functional')
rfther = importr('feather', on_conflict="warn")
rprll = importr('parallel')
rbase.options(robjects.vectors.ListVector({'mc.cores':rprll.detectCores()}))
#rbase.options(robjects.vectors.ListVector({'mc.cores':2}))


tobool_yrbs = robjects.r('''
function(col) {
    as.logical( 2 - col)
} ''')
class_yrbs = robjects.r('''
function(v) {
    class(v)
} ''')

factor_summary = robjects.r('''
function(v) {
    summary(as.factor(v))
}''')

class ParseCDCSurveyException(Exception):
    pass

def load_cdc_survey(dat_file, svy_cols, svy_vars):
    df = pd.read_fwf(dat_file, colspecs=list(svy_cols.values()),
                     names=list(svy_cols.keys()), na_values=['.',''])
    logging.info("Parsed raw survey data")
    rdf = com.convert_to_r_dataframe(df)
    logging.info("Converted survey data to R object")
    for q, v in svy_vars.items():
        if v['is_integer']:
            (codes, cats) = zip(*v['responses'])
            idx = rdf.colnames.index(q)
            fac = rdf[idx]
            try:
                fac = rbase.as_integer(fac)
                fac = rbase.factor(fac, levels=list(codes), labels=list(cats))
                rdf[idx] = fac
            except:
                logging.error(rbase.summary(rdf[idx]))
                logging.error(factor_summary(rdf[idx]))
                logging.error(rbase.summary(fac))
                bt.send_last_exception()
                raise ParseCDCSurveyException("parsing problems: %s -> %s"
                                              % (q, v))
        elif q.startswith('qn'):
            idx = rdf.colnames.index(q)
            fac = rbase.as_integer(rdf[idx])
            coerced = rbase.is_na(fac)
            n_coerced = rbase.sum(coerced)[0]
            if n_coerced > 0:
                coerced = factor_summary(rdf[idx].rx(coerced))
                logging.warning("Coerced non-numeric values for variable:" +
                                " %s\n%s" % (q, coerced))
            if rbase.min(fac, na_rm=True)[0] < 1 or \
               rbase.max(fac, na_rm=True)[0] > 2:
                raise ParseCDCSurveyException("Found invalid levels for" +
                                              " boolean var: %s -> %s" %
                                              (q, factor_summary(fac)))
            rdf[idx] = tobool_yrbs(fac)
    return rdf

spss_file = 'data/YRBS_2015_SPSS_Syntax.sps'
dat_file = 'data/yrbs2015.dat'

spss_file = 'data/2015-sadc-spss-input-program.sps'
dat_file = 'data/sadc_2015_national.dat'

svy_cols = cdc.parse_fwfcols_spss(spss_file)
svy_vars = cdc.parse_surveyvars_spss(spss_file)
logging.info("Parsed SPSS metadata")

rdf = None

try:
    rdf = rfther.read_feather('cache/yrbs.combined.feather')
    logging.info('Loaded survey data from feather cache...')
except:
    logging.warning("Could not find feather cache, loading raw data...")
    rdf = load_cdc_survey(dat_file, svy_cols, svy_vars)
    rfther.write_feather(rdf, 'cache/yrbs.combined.feather')

yrbsdes = rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
						 strata=Formula('~stratum'), data=rdf, nest=True)

#svyciprop_yrbs = rfunc.Curry(rsvy.svyciprop, method='xlogit', level=0.95,
#                             na_rm=True)
#svybyci_yrbs = rfunc.Curry(rsvy.svyby, keep_var=True, method='xlogit',
#                           vartype=robjects.vectors.StrVector(['se','ci']),
#                           na_rm_by=True, na_rm_all=True, multicore=True)
svyciprop_yrbs = robjects.r('''
function(formula, design, method='xlogit', level = 0.95, df=degf(design), ...) {
    svyciprop(formula, design, method, level, df, na.rm=TRUE, ...)
}''')

svybyci_yrbs = robjects.r('''
function( formula, by, des, fn, ...) {
    svyby(formula, by, des, fn, keep_var=TRUE, method='xlogit',
          vartype=c('se','ci'), na.rm.by=TRUE, na.rm.all=TRUE, multicore=TRUE)
}''')


filter_var_levels = robjects.r('''
function(des, k, vals){
    des$variables[[k]] %in% vals
}
''')


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
#extend Series with fill_none method
# to take care of json/mysql conversion
def fill_none(self):
    return self.where(pd.notnull(self),None)
pd.Series.fill_none = fill_none

#cache = LRUCache(maxsize=None)
#lock = RLock()


def subset(des, filt):
    #filt is a dict with vars as keys and list of acceptable values as levels
    #example from R:
    #  subset(dclus1, sch.wide=="Yes" & comp.imp=="Yes"
    if len(filt.keys()) == 0:
        return des
    filtered = rbase.Reduce( "&",
        [filter_var_levels(des, k, v) for k,v in filt.items()]
    )
    return rsvy.subset_survey_design(des, filtered)

def fetch_stats(des, qn, response=True, vars=[]):
    DECIMALS = {
        'mean': 4, 'se': 4, 'ci_l': 4, 'ci_u': 4, 'count':0
    }
    #def cache_key_fn(*args, **kwargs):
    #    v = ','.join(sorted(args[0]))
    #    q = args[1]
    #    return '%s:%s' % (v,q)

    #@cached(cache, key=cache_key_fn)
    def fetch_stats_by(vars, qn_f, des):
        lvl_f = Formula('~%s' % ' + '.join(vars))
        #svyciprop_local =
        merged = pandas2ri.ri2py(rbase.merge(
            svybyci_yrbs(qn_f, lvl_f, des, svyciprop_yrbs),
            rsvy.svyby(qn_f, lvl_f, des, rsvy.unwtd_count, na_rm=True,
                       na_rm_by=True, na_rm_all=True, multicore=True)
        ))
        del merged['se']
        merged.columns = vars + ['mean', 'se', 'ci_l', 'ci_u', 'count']
        merged['level'] = len(vars)
        merged['q'] = qn
        merged['q_resp'] = response
        merged = merged.round(DECIMALS)
        return merged.apply(lambda r: r.fill_none().to_dict(), axis=1)
    # create formula for selected question and risk profile
    # ex: ~qn8, ~!qn8
    #print(qn,response,vars,file=sys.stderr)
    qn_f = Formula('~%s%s' % ('' if response else '!', qn))
    count = rbase.as_numeric(rsvy.unwtd_count(qn_f, des, na_rm=True,
                                              multicore=True))[0]
    total_ci = None
    if count > 0:
        total_ci = svyciprop_yrbs(qn_f, des, multicore=True)
    #extract stats
    res = { 'level': 0,
           'mean': rbase.as_numeric(total_ci)[0],
           'se': rsvy.SE(total_ci)[0],
           'ci_l': rbase.attr(total_ci,'ci')[0],
           'ci_u': rbase.attr(total_ci,'ci')[1],
           'count': count }
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
    print(rbase.gc(), file=sys.stderr)
    print(gc.collect())
    return res

#idx = rdf.colnames.index('q3')

'''
print("setup complete", )
sys.stdout.flush()
def test_fn(iter):
    print("%d - run 1" % iter)
    sys.stdout.flush()
    print(fetch_stats(yrbsdes, 'qn8', True, ['race7', 'sex']))
    print("%d - run 2" % iter)
    sys.stdout.flush()
#    fetch_stats(yrbsdes, 'qn8', True, ['q2', 'q3', 'raceeth'])
#    print("%d - run 3" % iter)
#    sys.stdout.flush()
#    fetch_stats(yrbsdes, 'qn8', True, ['q2', 'raceeth'])

for i in range(1):
    test_fn(i)
#sys.exit()
#print(timeit.timeit('test_fn()', number=10))
'''
d = {'grade': ['11th', '12th'],
      'race7': ['White', 'Asian'],
      'year': ['2011', '2013', '2015']}

res = fetch_stats( subset(yrbsdes, d), 'qn8', True, ['sex'] )
print(res, file=sys.stderr)
res = fetch_stats( yrbsdes, 'qn8', True, ['sex'] )
print(res, file=sys.stderr)
META_COLS = ['year','questioncode','shortquestiontext','description',
			 'greater_risk_question','lesser_risk_question','topic','subtopic']

META_URL = 'https://chronicdata.cdc.gov/resource/6ay3-nik2.json'
META_URL += '?$select={0},count(1)&$group={0}'.format(','.join(META_COLS))

def fetch_qn_meta():
	query = (META_URL)
	m = pd.read_json(query).fillna('')
	m['questioncode'] = m.questioncode.apply( lambda k: k.replace('H','qn') if k[0]=='H' else k.lower() )
	del m['count_1']
	m.set_index(['year','questioncode'], inplace=True, drop=False)
	return m.to_dict(orient="index")

#app = Sanic(__name__)
from flask import Flask
from flask import request as req
from flask.json import jsonify

class InvalidUsage(Exception):

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class EmptyFilterError(Exception):

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class ComputationError(Exception):

    def __init__(self, message, status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv

app = Flask(__name__)
meta = fetch_qn_meta()

@app.errorhandler(InvalidUsage)
@app.errorhandler(EmptyFilterError)
@app.errorhandler(ComputationError)
def handle_invalid_usage(error):
    bt.send_last_exception()
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/questions")
@app.route("/questions/<year>")
def fetch_questions(year=2015):
	def get_meta(k, v, yr=year):
		key = (2015,k.lower())
		res = dict(meta[key], **v) if key in meta else v
		return res
	res = {k: get_meta(k,v) for k, v in svy_vars.items()}
	return jsonify(res)

@app.route('/stats')
@app.route('/stats/<sitecode>')
@app.route('/stats/<sitecode>/<year>')
def fetch_survey_stats(sitecode='XX', year='2015'):
    """TODO: reformat for swagger
    Computes survey stats for given binary response variable, breakout
    variables and population filters

    Route Parameters:
        sitecode: (required) sitecode for state/locality of interest -- use XX
        for national level survey data (ex: 'XX', 'PA', 'VA', 'MD')
        year: (default=combined) survey year, omit for combined survey across
        all years for given sitecode (questions correspond to latest year)
    URL Parameters:
        q: (required) question to compute stats for
        v: (default=None) variables to break out responses by (ex: 'sex,race')

        r: (default=1) response to binary question to compute SE and CI for,
        options=[1 -> True, 0 -> False]
        f: (default=None) subset the population using demographic variables,
        for example (f=sex:Male;race7:White,Asian;year=2011,2013,2015)

    Returns:
        stuff -- TODO: explain return structure
    """
    def validate_var_level(v,f):
        raise NotImplementedError('Validating variables and selected levels is'
                                  + 'not yet implemented, sorry bro!')
    qn = req.args.get('q')
    vars = [] if not 'v' in req.args else req.args.get('v').split(',')
    resp = True if not 'r' in req.args else int(req.args.get('r')) > 0
    filt = {} if not 'f' in req.args else dict(map(lambda fv:
                                                   (fv.split(':')[0],
                                                    fv.split(':')[1].split(',')),
                                                   req.args.get('f').split(';')))
    subs = subset(yrbsdes,filt)
    lsub = rbase.dim(subs[subs.names.index['variables']])[1]
    print("Filtered %d rows with filter: %s" % (lsub, str(filt)),
          file=sys.stderr)
    if not lsub > 1:
        raise EmptyFilterError("EmptyFilterError: %s" % (str(filt)))
    try:
        return jsonify({
            "q": qn,
            "question": svy_vars[qn]['question'],
            "response": resp,
            "vars": vars,
            "var_levels": {v: svy_vars[v] for v in vars},
            "results": fetch_stats(subs, qn, resp, vars)
        })
    except KeyError as  err:
        raise InvalidUsage('KeyError: %s' % str(err))
    except Exception as err:
        raise ComputationError('Error computing stats! %s' % str(err))


if __name__=='__main__':
    app.run(host="0.0.0.0", port=7777, debug=True)

