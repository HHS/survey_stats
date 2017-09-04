import pandas as pd
from odo import odo
import sqlalchemy as sa
import blaze as bz
import requests as rq

from sanic import Sanic
from sanic.config import Config
from sanic.response import json
from sanic.exceptions import InvalidUsage, ServerError
import dask
import dask.multiprocessing
import dask.cache
from multiprocessing.pool import ThreadPool
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
    dset = req.args.get('d')
    d = st.dset[dset]
    res = d.meta.groupby(['qid']).agg({
        'topic': lambda x: x.get_values()[0],
        'subtopic': lambda x: x.get_values()[0],
        'question': lambda x: x.get_values()[0],
        'response': lambda x: x.get_values()[0],
        'year': lambda x: list(x.drop_duplicates()),
        'sitecode': lambda x: list(x.drop_duplicates())
    }).reset_index()
    res.index = res['qid']
    facs = (d.meta.ix[d.cfg.facets]
            .groupby(['qid']).agg({
                'response': lambda x: x.get_values()[0]
            }).reset_index()
            .rename(
                index=str,
                columns={'qid':' facet',
                         'response': 'facet_levels'}
            ))
    #facs.index = facs.ix['qid']
    return json({'facets': facs.to_dict(orient='records'),
                 'questions': res.to_dict(orient='index')})


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


def parse_filter(f):
    return dict(map(lambda fv: (fv.split(':')[0],
                                fv.split(':')[1].split(',')),
                    f.split('|')))


def fetch_survey(dset, qn, filt, vars):
    ds = st.dset[dset]
    return ds.fetch_stats(qn, filt, vars)

@app.route('/stats')
def fetch_survey_stats(req):
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
            results = d.fetch_stats(qn, vars, filt)
        else:
            results = d.fetch_socrata(qn, vars, filt)
    except Exception as e:
        raise ServerError(e)
    # logger.info('dumping result', res=results)
    return json({
        'error': error,
        'q': qn,
        'filter': filt,
        'question': question,
        'vars': vars,
        'results': results.to_dict(orient='records')
    })


def setup_app(db_conf, stats_svc):
    app.config.db_conf = db_conf
    app.config.stats_svc = stats_svc
    dask.set_options(get=dask.threaded.get, pool=ThreadPool())
    return app


def serve_app(host, port, workers, stats_svc, debug):
    app.run(host=host, port=port, workers=workers, debug=debug)


if __name__ == '__main__':
    serve_app(host='0.0.0.0', port=7778, workers=1, debug=True)
