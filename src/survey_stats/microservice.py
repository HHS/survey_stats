import falcon
import ujson as json
from survey_stats import log
from survey_stats import state as st
# import traceback
# import falcon_jsonify
# from falcon import HTTPInvalidParam, HTTPMissingParam

logger = log.getLogger(__name__)

db_cfg = None
cache_dir = None


class HealthResource:

    def __init__(self):
        self.logger = log.getLogger('statsworker.' + __name__)

    def on_get(self, req, resp):
        import sqlalchemy as sa
        from rpy2 import robjects as ro
        from rpy2.robjects import r
        import blaze as bz
        engine = sa.create_engine(db_cfg.uri)
        dbc = bz.data(engine)
        dbinfo = {'host': dbc.data.engine.url.host,
                  'engine': dbc.data.engine.name,
                  'tables': dbc.fields,
                  'config': db_cfg}
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
                                   'Could not read the request body. Must be '
                                   'them ponies again.')

        try:
            slice = json.loads(raw_json, 'utf-8')
            self.logger.info(json.dumps(slice))
        except ValueError:
            raise falcon.HTTPBadRequest(
                'Malformed JSON',
                'Could not decode the request body. The '
                'JSON was incorrect.')
        try:
            d = slice['d']
            q = slice['q']
            r = slice['r']
            vs = slice['vs']
            f = slice['f']
            svy = st.dset[d]
            result = svy.fetch_stats_for_slice(q, r, vs, f).to_dict(orient='records')
            self.logger.info('got the results!', res=result)
        except Exception as ex:
            self.logger.error(ex)
            raise falcon.HTTPInternalServerError('StatsWorker Failure', ex)

        resp.set_header('X-Powered-By', 'Ninjas')
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'error': None, 'data': result})


def setup_app(dbc, cdir, use_feather):
    global db_cfg, cache_dir
    db_cfg = dbc
    cache_dir = cdir
    app = falcon.API()
    app.add_route('/stats', StatsResource())
    app.add_route('/', HealthResource())
    st.initialize(dbc, cdir, init_des=True, use_feather=use_feather, init_svy=False, init_soc=False)
    return app

# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=7788, debug=True)
