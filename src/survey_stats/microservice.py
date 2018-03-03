import traceback
import cattr
import attr
import flask_transmute
from flask import Flask, Blueprint
from flask_transmute import (
    route, annotate, Response, APIException
)
from typing import (
    Optional, Sequence, Callable, TypeVar, Mapping, Union, Dict, List
)
# from falcon import HTTPInvalidParam, HTTPMissingParam
from survey_stats import log
from survey_stats import state as st
from survey_stats.types import T

logger = log.getLogger(__name__)

db_cfg = None
cache_dir = None

app = Flask(__name__)


@attr.s
class SvySlice(object):
    d: str = attr.ib()
    q: str = attr.ib()
    r: str = attr.ib()
    vs: Sequence[str] = attr.ib()
    f: Mapping[str, Sequence[str]] = attr.ib()

@attr.s
class SvyStats(dict):
    pass


@route(app, body_parameters="s", paths='/stats', methods=['POST'])
def compute(s: SvySlice) -> [SvyStats]:
    try:
        svy = st.dset[s.d]
        result = (svy.fetch_stats_for_slice(s.q, s.r, s.vs, s.f)
                     .to_dict(orient='records'))
        logger.info('got the results!', res=result)
    except Exception as ex:
        raise APIException('worker failure!' +  str(ex))
    return result


def setup_app(dbc, cdir, use_feather):
    app.config.update(dbc=dbc, cache_dir=cdir)
    st.initialize(dbc, cdir, init_des=True,
                  use_feather=use_feather,
                  init_svy=False, init_soc=False)
    return app
