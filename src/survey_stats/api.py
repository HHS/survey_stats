import pandas as pd
import sqlalchemy as sa
import blaze as bz
import requests as rq
from cytoolz.itertoolz import concatv
from cytoolz.dicttoolz import assoc
from sanic import Sanic
from sanic.response import json
from sanic.config import Config
from sanic.exceptions import (
    SanicException, ServerError, NotFound, InvalidUsage, RequestTimeout
)
from survey_stats import log
from survey_stats import state as st
from survey_stats.const import MAX_CONCURRENT_REQ
import json as j
import asyncio
import aiohttp
import ujson
import traceback


app = Sanic(__name__)
logger = log.getLogger()
sem = None
headers = {'content-type': 'application/json'}
app.static('/favicon.ico', './static/favicon.ico')



class SurveyError(InvalidUsage):

    def __init__(self, message, info):
        self.info = info
        InvalidUsage.__init__(self, message=message)


@app.listener('before_server_start')
def init(sanic, loop):
    global sem
    sem = asyncio.Semaphore(MAX_CONCURRENT_REQ, loop=loop)


async def bound_fetch(url, data, session):
    async with sem, session.post(url, json=data, headers=headers) as response:
        logger.info('submitting async post request', url=response.url, data=data)
        return await response.json()


async def fetch_all(slices, worker_url, worker_socket=False):
    conn = None
    if worker_socket.startswith('/'):
        conn = aiohttp.UnixConnector(path=worker_socket, limit=MAX_CONCURRENT_REQ)
        worker_url = 'http://localhost' # + worker_socket 
    else:
        conn = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQ)
    rqurl = worker_url + '/stats'
    tasks = []
    # Create client session that will ensure we dont open new connection
    # per each request.
    async with aiohttp.ClientSession(connector=conn, json_serialize=ujson.dumps) as session:
        for s in slices:
            logger.info(sl=s, url=rqurl)
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(rqurl, s, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return [r for r in responses]


async def fetch_socrata(qn, resp, vars, filt, meta):
    precomp = meta.fetch_dash(qn, resp, vars, filt)
    precomp = pd.DataFrame(precomp).fillna(None)
    precomp['method'] = 'socrata'
    return precomp.to_dict(orient='record')


@app.exception(NotFound, ServerError, InvalidUsage, RequestTimeout)
def json_404s(request, exception):
    tb=traceback.format_exc()
    logger.info('Uh Oh! Encountered an error while fetching stats!', 
                error=exception, request=request, traceback=tb) 
    return json({'error': exception, 'traceback':tb})


@app.route("/")
async def check_status(req):
    # verify that the upstream services are functional
    engine = sa.create_engine(app.config.dbc.uri)
    db = bz.data(engine)
    dbinfo = {'host': db.data.engine.url.host,
              'engine': db.data.engine.name,
              'tables': db.fields,
              'config': app.config.dbc}
    r = None
    wrkinfo = None
    try:
        r = rq.get(app.config.stats_svc)
        wrkinfo = r.json()
        r = {'error': None, 'data': None}
    except Exception as e:
        raise ServerError(str(e))
    return json({'data':
                 {'db': dbinfo,
                  'worker_url': app.config.stats_svc,
                  'worker_status': wrkinfo
                  }})


@app.route("/questions")
async def fetch_questions(req):
    dset = req.args.get('d')
    d = st.dset[dset]
    return json({'facets': d.meta.facet_map,
                 'questions': d.meta.questions}) 


def parse_filter(f):
    return dict(map(lambda fv: (fv.split(':')[0],
                                fv.split(':')[1].split(',')),
                    f.split('|')))


async def fetch_stats(dset, qn, vars, filt):
    d = st.dset[dset]
    slices = d.generate_slices(qn, vars, filt)
    return await fetch_all(slices, app.config.stats_svc, app.config.stats_sock)


@app.route('/stats')
async def fetch_survey_stats(req):
    try:
        dset = req.args.get('d')
    except KeyError as e:
        raise SurveyError(str(e), 
                           info={'datasets': list(dset.keys())})
    d = st.dset[dset]
    qs = d.meta.questions
    fs = d.meta.facet_map
    qn = req.args.get('q')
    if qn not in qs:
        raise SurveyError("Cannot find qid: %s in dataset: %s" % (qn, dset),
                           info={'questions': list(qs.keys())})
    vars = [] if 'v' not in req.args else req.args.get('v').split(',')
    for v in vars:
        if not v in d.meta.vars:
            raise SurveyError("Cannot find var facet v: %s in dataset: %s" % (v, dset),
                               info={'facets': fs})
    filt = {} if 'f' not in req.args else parse_filter(req.args.get('f'))
    for k, vals in filt.items():
        if not k in fs:
            raise SurveyError("Cannot find filter facet: %s in dataset: %s" % (k, dset),
                               info={'facets': fs})
        for v in vals:
            if not v in fs[k]:
                raise SurveyError("Cannot find value: %s for filter facet: %s in dataset: %s" % (v, k, dset),
                                   info={'facets': fs})

    use_socrata = False if 's' not in req.args else not 0 ** int(req.args.get('s'), 2)
    if use_socrata and not d.meta.has_socrata:
        raise SurveyError("Socrata pre-computed data not available for dataset: %s" % dset, info={'facets': fs})
    if not use_socrata and not d.meta.has_surveys:
        raise SurveyError("Surveys data not available for dataset: %s" % dset, info={'facets': fs})

    question = qn  # meta.qnmeta[qn]
    results = None  # fetch_socrata(qn, resp, vars, filt, national, meta)
    error = None
    try:
        if not use_socrata:
            results = await fetch_stats(dset, qn, vars, filt)
            results = concatv(*results)
            for v in vars:
                results = map(lambda d: d if v in d else assoc(d, v, 'Total'), results)
        else:
            results = d.fetch_socrata(qn, vars, filt)
            results = results.to_dict(orient='records')
    except Exception as e:
        raise ServerError(e)
    # logger.info('dumping result', res=results)
    return json({
        'error': error,
        'q': qn,
        'filter': filt,
        'question': question,
        'vars': vars,
        'results': results
    })


def setup_app(dbc, cache_dir, stats_svc, sanic_timeout, use_feather, worker_socket):
    app.config.dbc = dbc
    app.config.cache = cache_dir
    app.config.stats_svc = stats_svc
    app.config.sanic_timeout = sanic_timeout
    app.config.use_feather = use_feather
    app.config.stats_sock = worker_socket
    Config.REQUEST_TIMEOUT = sanic_timeout
    Config.KEEP_ALIVE = False
    logger.info('initializing state', dbc=dbc, cdir=cache_dir, f=use_feather)
    st.initialize(dbc, cache_dir, init_des=False, use_feather=use_feather, init_svy=True, init_soc=True)
    return app


def startup_app(app, loop):
    # TODO: deal with open connections
    pass


def teardown_app(app, loop):
    # TODO: deal with db conns
    # http://docs.sqlalchemy.org/en/latest/core/connections.html
    pass


def serve_app(host, port, workers, debug):
    app.run(host=host, port=port, workers=workers,
            timeout=app.config.sanic_timeout,
            reuse_port=True, debug=debug)


if __name__ == '__main__':
    serve_app(host='0.0.0.0', port=7778, workers=1, debug=True)
