import sys
import rq
from rq.decorators import job
from redis import Redis

from survey_stats.error import InvalidUsage, EmptyFilterError, ComputationError
from survey_stats import settings
from survey_stats import state as st
import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

rq.use_connection(Redis())


'''
async def run_task(task, *args, loop=None, **kwargs):
    Returns job result or None if an error occurs
    job = task.delay(*args, **kwargs)
        return job.result
    #  while True:
    for i in range(100000):
        print(i, file=sys.stderr)
        await asyncio.sleep(0.01, loop=loop)
        if job.is_finished:
            return job.result
        if job.is_failed:
            raise Exception('Job is failed')
'''


@job('high')
def task_get_questions(year=None):
    pass


@job('low')
def task_fetch_slice_stats(qn_f, filt_f, slice_f, svy_id, dset_id='yrbss'):

    svy = st.dset[dset_id].surveys[svy_id]
    return svy.fetch_stats_for_slice(qn_f, filt_f, slice_f)
