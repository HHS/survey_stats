import logging
import falcon
import ujson as json
import traceback
from falcon import HTTPInvalidParam, HTTPMissingParam
from survey_stats import log
from survey_stats import settings
from survey_stats import state as st


logger = log.getLogger(__name__)

def check_media_type(req, resp, params):
    if req.client_accepts_json:
        return
    raise falcon.HTTPUnsupportedMediaType(
        'Media Type not Supported',
        'This API only supports the JSON media type.',
        'http://docs.examples.com/api/json')





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
            d = slice['d']
            q = slice['q']
            r = slice['r']
            vs = slice['vs']
            f = slice['f']
            svy = st.dset[d]
            result = svy.fetch_stats_for_slice(q, r, vs, f).to_dict(orient='records')
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
        d = req.get_param('d')
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
        try:
            svy = st.dset[d]
            result = svy.fetch_stats_for_slice(q, r, vs, f).to_dict(orient='records')
        except KeyError as err:
            raise HTTPInvalidParam('KeyError: %s' % str(err), payload={
                'traceback': traceback.format_exc().splitlines(),
                'state': {'q': qn, 'filter': filt, 'response': resp, 'var_levels': var_levels
                          }})
        resp.set_header('X-Powered-By', 'Ninjas')
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)

def setup_app(dbc, cache):
    app = falcon.API()
    app.add_route('/stats', StatsResource())
    app.add_route('/', HealthResource())
    st.initialize(dbc, cache)
    return app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7788, debug=True)
