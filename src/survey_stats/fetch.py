import logging
import random
import uvloop
import asyncio
import json
from aiohttp import ClientSession

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

MAX_CONCURRENT_REQ = 1000
headers = {'content-type': 'application/json'}

async def fetch(url, data, session):
	async with session.get(url, data=json.dumps(data), headers=headers) as response:
		delay = response.headers.get('DELAY')
		date = response.headers.get('DATE')
		print('{}:{} with delay {}'.format(date, response.url, delay))
		return await response.json()


async def fetch_all(slices):
	rqurl = 'http://localhost:7788/stats'
	tasks = []

	# Create client session that will ensure we dont open new connection
	# per each request.
	async with ClientSession() as session:
		for s in slices:
			logging.info(s)
			# pass Semaphore and session to every GET request
			task = asyncio.ensure_future(fetch(rqurl, s, session))
			tasks.append(task)

		responses = await asyncio.gather(*tasks)
		print(responses)
		return [r for r in responses]
