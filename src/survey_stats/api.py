import pandas as pd
import sqlalchemy as sa
import blaze as bz
import requests as rq
from cytoolz.curried import curry
from cytoolz.itertoolz import concatv
from cytoolz.dicttoolz import assoc, valmap, keyfilter
from cytoolz.functoolz import thread_last
from sanic import Sanic
from sanic.response import json
from sanic.config import Config
from sanic.exceptions import ServerError
from survey_stats import log
from survey_stats import state as st
from survey_stats import fetch
from survey_stats import pdutil as pdu

Config.REQUEST_TIMEOUT = 50000000

app = Sanic(__name__)
dbc = None
logger = log.getLogger()


async def fetch_socrata(qn, resp, vars, filt, meta):
    precomp = meta.fetch_dash(qn, resp, vars, filt)
    precomp = pd.DataFrame(precomp).fillna(None)
    precomp['method'] = 'socrata'
    return precomp.to_dict(orient='record')


def get_first_aggval(xf):
    return xf.get_values()[0]


def get_drop_dup_aggvals(xf):
    return list(xf.drop_duplicates())


@app.route("/questions")
async def fetch_questions(req):
    dset = req.args.get('d')
    d = st.dset[dset]
    rem = ['qid', 'sitecode', 'facet', 'facet_level'] + d.cfg.facets
    drops = ['response', 'year']
    dkeys = set(d.cfg.socrata.qn_meta).difference(rem)
    aggd = {k: get_drop_dup_aggvals if
            k in drops else get_first_aggval
            for k in dkeys}
    res = (d.meta.qns
           .groupby(['qid'])
           .agg(aggd)
           .reset_index()
           .pipe(lambda xf: pdu.fill_none(xf))
           .set_index(['qid'])
           .to_dict(orient='index'))
    facs = (d.meta.facets
            .groupby(['facet'])
            .agg({'facet_level':
                  lambda x: list(x.drop_duplicates())})
            .pipe(lambda xf: pdu.fill_none(xf))
            .to_dict(orient='index'))
    facs = thread_last(facs,
                       curry(valmap)(lambda x: x['facet_level']),
                       curry(keyfilter)(lambda x: x != 'Overall'))
    return json({'facets': facs,
                 'questions': res})


@app.route("/")
async def check_status(req):
    # verify that the upstream services are functional
    engine = sa.create_engine(app.config.dbc.url)
    db = bz.data(engine)
    dbinfo = {'host': db.data.engine.url.host,
              'engine': db.data.engine.name,
              'tables': db.fields}
    r = rq.get(app.config.stats_svc)
    wrkinfo = r.json()
    return json({'db': dbinfo,
                 'worker_url': app.config.stats_svc,
                 'worker_status': wrkinfo})


def parse_filter(f):
    return dict(map(lambda fv: (fv.split(':')[0],
                                fv.split(':')[1].split(',')),
                    f.split('|')))


async def fetch_stats(dset, qn, vars, filt):
    d = st.dset[dset]
    slices = d.generate_slices(qn, vars, filt)
    return await fetch.fetch_all(slices, app.config.stats_svc)


@app.route('/stats')
async def fetch_survey_stats(req):
    dset = req.args.get('d')
    qn = req.args.get('q')
    vars = [] if 'v' not in req.args else req.args.get('v').split(',')
    filt = {} if 'f' not in req.args else parse_filter(req.args.get('f'))
    use_socrata = False if 's' not in req.args else not 0 ** int(req.args.get('s'), 2)
    d = st.dset[dset]
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


def setup_app(dbc, cache_dir, stats_svc, sanic_timeout):
    app.config.dbc = dbc
    app.config.cache = cache_dir
    app.config.stats_svc = stats_svc
    app.config.sanic_timeout = sanic_timeout
    st.initialize(dbc, cache_dir)
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
