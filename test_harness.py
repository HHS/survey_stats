from __future__ import print_function
import sys
import backtracepython as bt
import numpy as np
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


rbase.gc()
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
    lsub = rbase.dim(subs[subs.names.index('variables')])[0]
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

