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

from survey import AnnotatedSurvey
from datasets import SurveyDataset

logging.basicConfig(level=logging.DEBUG)

META_COLS = ['questioncode','shortquestiontext','description',
			 'greater_risk_question','lesser_risk_question','topic','subtopic']

META_URL = 'https://chronicdata.cdc.gov/resource/6ay3-nik2.json'
META_URL += '?$select={0},count(1)&$group={0}'.format(','.join(META_COLS))

def fetch_qn_meta():
	query = (META_URL)
	m = pd.read_json(query).fillna('')
	m['questioncode'] = m.questioncode.apply( lambda k: k.replace('H','qn') if k[0]=='H' else k.lower() )
	del m['count_1']
	m.set_index('questioncode', inplace=True, drop=False)
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
yrbss = SurveyDataset.load_dataset('data/yrbss.yaml')


@app.errorhandler(InvalidUsage)
@app.errorhandler(EmptyFilterError)
@app.errorhandler(ComputationError)
def handle_invalid_usage(error):
    bt.send_last_exception()
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/questions")
@app.route("/questions/<int:year>")
def fetch_questions(year=None):
    def get_meta(k, v):
        key = k.lower()
        res = dict(meta[key], **v) if key in meta else v
        return res
    combined = True
    national = True
    if year and year in range(1993, 2017, 2):
        combined = False
    dset = yrbss.fetch_survey(combined, national, year)
    res = {k: get_meta(k,v) for k, v in dset.vars.items()}
    return jsonify(res)


@app.route('/stats/national')
@app.route('/stats/national/<int:year>')
def fetch_national_stats(year=None):
    return fetch_survey_stats(national=True, year=year)


@app.route('/stats/state')
def fetch_state_stats(year=None):
    return fetch_survey_stats(national=False, year=None)


def fetch_survey_stats(national, year):
    logging.info("requested uri: %s" % req.url)
    qn = req.args.get('q')
    vars = [] if not 'v' in req.args else req.args.get('v').split(',')
    resp = True if not 'r' in req.args else int(req.args.get('r')) > 0
    filt = {} if not 'f' in req.args else dict(map(lambda fv:
                                                   (fv.split(':')[0],
                                                    fv.split(':')[1].split(',')),
                                                    req.args.get('f').split(';')))

    logging.info(filt)
    combined = True
    if year and year in range(1993, 2017, 2):
        combined = False

    # update vars and filt column names according to pop_vars
    (k, cfg) = yrbss.fetch_config(combined, national, year)
    logging.info((k, cfg))
    replace_f = lambda x: cfg['pop_vars'][x] if x in cfg['pop_vars'] else x
    logging.info(vars)
    logging.info(filt)
    m_vars = list(map(replace_f, vars))
    m_filt = {replace_f(k): v for k,v in filt.items()}
    svy = yrbss.surveys[k]
    svy = svy.subset(m_filt)

    if not svy.sample_size > 1:
        raise EmptyFilterError('EmptyFilterError: %s' % (str(m_filt)))
    ivd = {v: k for k, v in cfg['pop_vars'].items()}

    #setup functions to reverse map keys for stats
    inverse_f = lambda x: ivd[x] if x in ivd else x
    replkeys_f = lambda d: {inverse_f(k): v for k,v in d.items()}

    try:
        stats = svy.fetch_stats(qn, resp, m_vars)
        stats = list(map(replkeys_f, stats))
        return jsonify({
            'q': qn,
            'question': svy.vars[qn]['question'],
            'response': resp,
            'vars': vars,
            'var_levels': {inverse_f(v): svy.vars[v] for v in m_vars},
            'results': stats
        })
    except KeyError as  err:
        raise InvalidUsage('KeyError: %s' % str(err))
    except Exception as err:
        raise ComputationError('Error computing stats! %s' % str(err))


if __name__=='__main__':
    app.run(host="0.0.0.0", port=7777, debug=True)

