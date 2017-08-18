import pandas as pd
import blaze as bz
from odo import odo

from toolz.dicttoolz import merge

from sanic import Sanic
from sanic.config import Config
from sanic.response import text, json
from sanic.exceptions import InvalidUsage, ServerError, NotFound

from survey_stats import log
from survey_stats import settings
from survey_stats import fetch
from survey_stats import state as st



Config.REQUEST_TIMEOUT = 50000000

app = Sanic(__name__)
dbc = None

logger = log.getLogger()

async def fetch_computed(k, svy, qn, resp, m_vars, m_filt, cfg, wrk):
    slices = gen_slices(k, svy, qn, resp, m_vars, m_filt)
    results = await fetch.fetch_all(slices, wrk)
    results = [remap_vars(cfg, x, into=False) for x in results]
    return results

async def fetch_socrata(qn, resp, vars, filt, meta):
    precomp = meta.fetch_dash(qn, resp, vars, filt)
    precomp = pd.DataFrame(precomp).fillna(-1)
    precomp['method']='socrata'
    return precomp.to_dict(orient='records')


@app.route("/questions")
async def fetch_questions(req):
    res = {"hello":"hello"}
    return json(res)

@app.route("/")
async def check_status(req):
	# verify that the upstream services are functional
	import pymonetdb
	import sqlalchemy_monetdb
	import sqlalchemy as sa
	import blaze as bz
	import requests as rq
	import json as js
	engine = sa.create_engine(app.config.db_conf['url'])
	dbc = bz.data(engine)
	dbinfo = { 'host': dbc.data.engine.url.host,
			   'engine': dbc.data.engine.name,
			   'tables': dbc.fields
			 }
	r = rq.get(app.config.stats_svc)
	wrkinfo = r.json()
	return json({'db': dbinfo,
				 'worker': wrkinfo})



def parse_filter(f):
    return dict(map(lambda fv: (fv.split(':')[0],
                                fv.split(':')[1].split(',')), f.split('|')))

def parse_response(r):
    if r.lower() == 'yes' or r.lower() == 'true' or r.lower() == '1':
        return True
    elif r.lower() == 'no' or r.lower() == 'false' or r.lower() == '0':
        return False
    else:
        raise Exception('Invalid response value specified!')

@app.route('/stats')
async def fetch_survey_stats(req):
    dset = req.args.get('d')
    qn = req.args.get('q')
    vars = [] if not 'v' in req.args else req.args.get('v').split(',')
    resp = None if not 'r' in req.args else parse_response(req.args.get('r'))
    filt = {} if not 'f' in req.args else parse_filter(req.args.get('f'))
    use_socrata = False if not 's' in req.args else not 0 ** int(req.args.get('s'), 2)
    meta = st.meta[dset]
    question = qn #meta.qnmeta[qn]
    results = None #fetch_socrata(qn, resp, vars, filt, national, meta)
    error = None
    #try:
    if not use_socrata:
        (k, cfg) = st.dset[dset].fetch_config(national=True, year=None)
        svy = st.dset[dset].surveys[k]
        m_filt = remap_vars(cfg, filt, into=True)
        m_vars = remap_vars(cfg, vars, into=True)
        if not svy.subset(m_filt).sample_size > 1:
            raise SSEmptyFilterError('EmptyFilterError: %s' % (str(m_filt)))
        question = svy.vars[qn]['question']
        var_levels = remap_vars(cfg, {v: svy.vars[v] for v in m_vars}, into=False)
        results = await fetch_computed(k, svy, qn, resp, m_vars, m_filt, cfg, app.config.stats_svc)
    else:
        results = fetch_socrata(qn, resp, vars, filt, meta)
    #except Exception as e:
    #    error = str(e)
    return json({
        'error': error,
        'q': qn,
        'filter': filt,
        'question': question,
        'response': resp,
        'vars': vars,
        'var_levels': None, #var_levels,
        'results': results,
        'is_socrata':use_socrata
    })



def setup_app(db_conf, stats_svc):
    app.config.db_conf = db_conf
    app.config.stats_svc = stats_svc
    return app


def serve_app(host, port, workers, stats_svc, debug):
    app.run(host=host, port=port, workers=workers, debug=debug)

if __name__ == '__main__':
    serve_app(host='0.0.0.0', port=7778, workers=1, debug=True)
