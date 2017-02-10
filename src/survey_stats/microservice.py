import logging
import falcon
import ujson as json
from survey_stats import log
from survey_stats import cache
from survey_stats import settings
from survey_stats import state as st
from threading import RLock
from functools import partial

def check_media_type(req, resp, params):
    if req.client_accepts_json:
        return
    raise falcon.HTTPUnsupportedMediaType(
        'Media Type not Supported',
        'This API only supports the JSON media type.',
        'http://docs.examples.com/api/json')

@cache.memoize
def fetch_svy_stats_for_slice(dset_id, svy_id, q, r, f, s ):
    ds = st.dset[dset_id]
    svy = ds.surveys[svy_id]
    res = svy.fetch_stats_for_slice(q, r, f, s)
    return res


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
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
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

app = falcon.API()
app.add_route('/stats', StatsResource())


'''
        try:
            proper_thing = self.db.add_thing(thing)

        except StorageError:
            raise falcon.HTTPError(falcon.HTTP_725,
                                   'Database Error',
                                   "Sorry, couldn't write your thing to the "
                                   'database. It worked on my machine.')
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7788, debug=True)
