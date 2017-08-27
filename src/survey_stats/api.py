import pandas as pd

import sqlalchemy as sa
import blaze as bz
import requests as rq

from sanic import Sanic
from sanic.config import Config
from sanic.response import json
from sanic.exceptions import InvalidUsage, ServerError

from survey_stats import log
from survey_stats import state as st

Config.REQUEST_TIMEOUT = 50000000

app = Sanic(__name__)
dbc = None

logger = log.getLogger()


async def fetch_socrata(qn, resp, vars, filt, meta):
    precomp = meta.fetch_dash(qn, resp, vars, filt)
    precomp = pd.DataFrame(precomp).fillna(-1)
    precomp['method'] = 'socrata'
    return precomp.to_dict(orient='records')


@app.route("/questions")
async def fetch_questions(req):
    res = {"hello": "hello"}
    return json(res)


@app.route("/")
async def check_status(req):
    # verify that the upstream services are functional
    engine = sa.create_engine(app.config.db_conf['url'])
    dbc = bz.data(engine)
    dbinfo = {'host': dbc.data.engine.url.host,
              'engine': dbc.data.engine.name,
              'tables': dbc.fields}
    r = rq.get(app.config.stats_svc)
    wrkinfo = r.json()
    return json({'db': dbinfo,
                 'worker': wrkinfo})


async def parse_filter(f):
    return dict(map(lambda fv: (fv.split(':')[0],
                                fv.split(':')[1].split(',')),
                    f.split('|')))


async def fetch_survey(dset, qn, filt, vars):
    (k, cfg) = st.dset[dset].fetch_config()
    svy = st.dset[dset].surveys[k]
    if not svy.subset(filt).sample_size >= 1:
        raise InvalidUsage('All rows filtered out! %s' % (str(filt)))
    return await fetch_computed(k, svy, qn, vars, filt, cfg, app.config.stats_svc)


@app.route('/stats')
async def fetch_survey_stats(req):
    dset = req.args.get('d')
    qn = req.args.get('q')
    vars = [] if 'v' not in req.args else req.args.get('v').split(',')
    filt = {} if 'f' not in req.args else parse_filter(req.args.get('f'))
    use_socrata = False if 's' not in req.args else not 0 ** int(req.args.get('s'), 2)
    meta = st.meta[dset]
    question = qn  # meta.qnmeta[qn]
    results = None  # fetch_socrata(qn, resp, vars, filt, national, meta)
    error = None
    try:
        if not use_socrata:
            results = fetch_survey(qn, vars, filt, meta)
        else:
            results = fetch_socrata(qn, vars, filt, meta)
    except Exception as e:
        raise ServerError(e)
    return json({
        'error': error,
        'q': qn,
        'filter': filt,
        'question': question,
        'vars': vars,
        'results': results,
        'is_socrata': use_socrata
    })


def setup_app(db_conf, stats_svc):
    app.config.db_conf = db_conf
    app.config.stats_svc = stats_svc
    return app


def serve_app(host, port, workers, stats_svc, debug):
    app.run(host=host, port=port, workers=workers, debug=debug)


if __name__ == '__main__':
    serve_app(host='0.0.0.0', port=7778, workers=1, debug=True)
