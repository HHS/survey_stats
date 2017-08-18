import logging
import falcon
import ujson as json
import traceback
from falcon import HTTPInvalidParam, HTTPMissingParam
from survey_stats import log
from survey_stats import settings

db_cfg = None

logger = log.getLogger(__name__)

def check_media_type(req, resp, params):
    if req.client_accepts_json:
        return
    raise falcon.HTTPUnsupportedMediaType(
        'Media Type not Supported',
        'This API only supports the JSON media type.',
        'http://docs.examples.com/api/json')


def fetch_svy_stats_for_slice(dset_id, svy_id, q, r, f, s):
    (k, cfg) = st.dset[dset_id].fetch_config(national=True, year=None)
    svy = st.dset[dset_id].surveys[k]
    res = svy.fetch_stats_for_slice(q, r, f, s, cfg)
    return res


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


class HealthResource:

	def __init__(self):
		self.logger = log.getLogger('statsworker.' + __name__)

	def on_get(self, req, resp):
		import pymonetdb
		import sqlalchemy_monetdb
		import sqlalchemy as sa
		from rpy2 import robjects as ro
		from rpy2.robjects import r
		import blaze as bz
		engine = sa.create_engine(db_cfg['url'])
		dbc = bz.data(engine)
		dbinfo = { 'host': dbc.data.engine.url.host,
				   'engine': dbc.data.engine.name,
				   'tables': dbc.fields
				 }
		clsf = r('''function(x){class(x)}''')
		rclass = lambda x: list(clsf(ro.globalenv[x]))[-1]
		robjs = dict(map(
					lambda x: (x, rclass(x)),
					r.ls(ro.globalenv)))
		resp.body = json.dumps({'alive': True,
					 'db': dbinfo,
					 'r': robjs})

class StatsResource:


    def __init__(self):
        self.logger = log.getLogger('statsworker.' + __name__)


    def on_post(self, req, resp):
        try:
            raw_json = req.stream.read()
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_748,
                                   'Read Error',
                                   'Could not read the request body. Must be '+
                                   'them ponies again.')

        try:
            slice = json.loads(raw_json, 'utf-8')
            self.logger.info(json.dumps(slice))
        except ValueError:
            raise falcon.HTTPBadRequest(
                'Malformed JSON',
                'Could not decode the request body. The ' +
                'JSON was incorrect.')
        try:
            result = fetch_svy_stats_for_slice(**slice)
        except Exception as ex:
            self.logger.error(ex)
            description = ('Aliens have attacked our base! We will '
                           'be back as soon as we fight them off. '
                           'We appreciate your patience.')

            raise falcon.HTTPServiceUnavailable(
              'Service Outage',
              description,
              30)

        resp.set_header('X-Powered-By', 'Ninjas')
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)


    def on_get(self, req, resp):
        self.logger.info("requested uri: %s" % req.url)
        qn = req.get_param('q')
        vars = req.get_param('v') or ''
        vars = vars.split(',')
        resp = req.get_param('r') or None
        filt = req.get_param('f') or ''
        filt = dict(map(
                lambda fv: (fv.split(':')[0],
                            fv.split(':')[1].split(',')),
                filt.split(';')
        )) if len(filt) > 0 else {}
        combined = True
        # update vars and filt column names according to pop_vars
        ds = st.dset['yrbss']
        (k, cfg) = ds.fetch_config(national=True, year=None)
        m_filt = remap_vars(cfg, filt, into=True)
        m_vars = remap_vars(cfg, vars, into=True)
        svy = ds.surveys[k]
        svy = svy.subset(m_filt)

        if not svy.sample_size > 1:
            raise ValueError('given filter is empty: %s' % (str(m_filt)))
        try:
            question = svy.vars[qn]['question']

        except KeyError as err:
            raise HTTPInvalidParam('invalid %s' % str(err), payload={
                'traceback': traceback.format_exc().splitlines(),
                'state': {'q': qn, 'svy_vars': svy.vars, 'm_vars': m_vars
                          }})
        try:
            results = svy.fetch_stats(qn, resp, m_vars, m_filt)
            results = [remap_vars(cfg, x, into=False) for x in results]
            return json({
                'response': resp, 'vars': vars,
                'var_levels': vars, 'results': stats
            })
        except KeyError as err:
            raise HTTPInvalidParam('KeyError: %s' % str(err), payload={
                'traceback': traceback.format_exc().splitlines(),
                'state': {'q': qn, 'svy_vars': svy.vars, 'm_vars': m_vars,
                          'filter': filt, 'response': resp, 'var_levels': var_levels
                          }})


def setup_app(db_conf):
    global db_cfg
    app = falcon.API()
    app.add_route('/stats', StatsResource())
    app.add_route('/', HealthResource())
    db_cfg = db_conf
    logger.info('booting worker with db', db=db_conf)
    return app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7788, debug=True)
