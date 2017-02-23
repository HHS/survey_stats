import time
import logging
import traceback
import pandas as pd
import numpy as np

from collections import OrderedDict
from collections.abc import Sequence
from collections.abc import Mapping
from toolz.dicttoolz import merge

from sanic import Sanic
from sanic.config import Config
from sanic.response import text, json

from survey_stats.log import logger
from survey_stats import error as sserr
from survey_stats import settings
from survey_stats import fetch
from survey_stats import state as st
from survey_stats.processify import processify

Config.REQUEST_TIMEOUT = 50000000

app = Sanic(__name__)

dset_id = 'yrbss'


@app.route("/questions")
def fetch_questions(req):
    def get_meta(k, v):
        key = k.lower()
        res = (dict(st.meta[dset_id].qnmeta_dict[key], **v, id=k) if key in
               st.meta[dset_id].qnmeta_dict else dict(v, id=k))
        return res
    national = True
    combined = True
    svy = st.dset[dset_id].fetch_survey(combined, national, year=None)
    res = [(k, get_meta(k, v)) for k, v in svy.vars.items()]
    res = OrderedDict(res)
    return json(res)


@app.route('/stats/national')
def fetch_national_stats(req):
    """
    National API
    Returns mean, CI and unweighted count for a national survey
    segment from either the combined or individual yearly datasets.
    """
    return fetch_survey_stats(req, national=True, year=None)


@app.route('/stats/state')
def fetch_state_stats(req):
    """
    State API

    segment from either the combined or individual yearly datasets.
    """
    return fetch_survey_stats(req, national=False, year=None)


def remap_vars(cfg, coll, into=True):
    def map_if(pv, k):
        return pv[k] if k in pv else k
    pv = ({v: k for k, v in cfg['pop_vars'].items()} if
          not into else cfg['pop_vars'])
    res = None
    typ = type(coll)
    if isinstance(coll, str):
        res = coll
    elif isinstance(coll, Sequence):
        res = [map_if(pv, k) for k in coll]
    elif isinstance(coll, Mapping):
        res = {map_if(pv, k): remap_vars(cfg, v, into) for
               k, v in coll.items()}
    else:
        res = coll
    return res

def gen_slices(k, svy, qn, resp, m_vars, m_filt):
    loc = {'svy_id': k, 'dset_id': 'yrbss'}
    slices = [merge(loc, s)
              for s in svy.generate_slices(qn, resp, m_vars, m_filt)]
    return slices

async def fetch_computed(k, svy, qn, resp, m_vars, m_filt, cfg):
    slices = gen_slices(k, svy, qn, resp, m_vars, m_filt)
    results = await fetch.fetch_all(slices)
    results = [remap_vars(cfg, x, into=False) for x in results]
    return results

def fetch_socrata(qn, resp, vars, filt, national, year, meta):
    logger.info("hello")
    precomp = meta.fetch_dash(qn, resp, vars, filt, national, year)
    precomp = pd.DataFrame(precomp).fillna(-1).to_dict(orient='records')
    return precomp

async def fetch_survey_stats(req, national, year):
    (k, cfg) = st.dset['yrbss'].fetch_config(national, year)
    qn = req.args.get('q')
    vars = [] if not 'v' in req.args else req.args.get('v').split(',')
    resp = True if not 'r' in req.args else not 0 ** int(req.args.get('r'), 2)
    filt = {} if not 'f' in req.args else dict(
        map(lambda fv: (fv.split(':')[0],
                        fv.split(':')[1].split(',')),
            req.args.get('f').split(';')))
    use_socrata = False if not 's' in req.args else not 0 ** int(req.args.get('s'), 2)
    svy = st.dset['yrbss'].surveys[k]
    meta = st.meta['yrbss']
    m_filt = remap_vars(cfg, filt, into=True)
    m_vars = remap_vars(cfg, vars, into=True)
    if not svy.subset(m_filt).sample_size > 1:
        raise EmptyFilterError('EmptyFilterError: %s' % (str(m_filt)))
    try:
        question = svy.vars[qn]['question']
        var_levels = remap_vars(
            cfg, {v: svy.vars[v] for v in m_vars}, into=False)
    except KeyError as err:
        raise sserr.SSInvalidUsage('KeyError: %s' % str(err), payload={
            'traceback': traceback.format_exc().splitlines(),
            'request': req.args,
            'state': {
                'q': qn,
                'svy_vars': svy.vars,
                'm_vars': m_vars
            }})
    try:
        logger.info("Ready to fetch!")
        # results = await fetch.fetch_all([])
        results = (await fetch_computed(k, svy, qn, resp, m_vars, m_filt, cfg) if not
                    use_socrata else fetch_socrata(qn, resp, vars, filt,
                                                   national, year, meta))
        return json({
            'q': qn,
            'filter': filt,
            'question': question,
            'response': resp,
            'vars': vars,
            'var_levels': var_levels,
            'results': results,
            'is_socrata':use_socrata,
            'precomputed': fetch_socrata(qn, resp, vars, filt, national, year,
                                         meta) if not use_socrata else []
        })
    except KeyError as err:
        raise sserr.SSInvalidUsage('KeyError: %s' % str(err), payload={
            'traceback': traceback.format_exc().splitlines(),
            'request': req.args,
            'state': {
                'q': qn,
                'svy_vars': svy.vars,
                'm_vars': m_vars,
                'filter': filt,
                'response': resp,
                'var_levels': var_levels
            }})


def serve_app(host, port, workers, debug):
    app.run(host=host, port=port, workers=workers, debug=debug)

if __name__ == '__main__':
    serve_app(host='0.0.0.0', port=7778, workers=1, debug=True)
