import uvloop
import asyncio
import ujson as json
from aiohttp import ClientSession
from survey_stats import log

logger = log.getLogger()

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

MAX_CONCURRENT_REQ = 5
headers = {'content-type': 'application/json'}


async def fetch_computed(url, data, session):
    async with session.post(url, data=data, headers=headers) as response:
        delay = response.headers.get('DELAY')
        date = response.headers.get('DATE')
        print('{}:{}, data={}, delay={}'.format(date, response.url, data, delay))
        try:
            return await response.json()
        except Exception as e:
            return {'error': str(e)}


async def fetch_all(slices, worker_url):
    rqurl = worker_url + '/stats'
    tasks = []

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for s in slices:
            print(json.dumps(s))
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(fetch_computed(rqurl, json.dumps(s), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return [r for r in responses]
