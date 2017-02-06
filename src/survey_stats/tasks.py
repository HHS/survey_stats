import sys
from rq.decorators import job
from rq import Queue
from redis import Redis
from rq import Connection, Worker

from survey_stats.survey import AnnotatedSurvey
from survey_stats.datasets import YRBSSDataset
from survey_stats.meta import SurveyMetadata
from survey_stats.error import InvalidUsage, EmptyFilterError, ComputationError
from survey_stats import settings
from survey_stats import state


#fetch the state.metadata from Socrata
meta = SurveyMetadata.load_metadata('data/yrbss.yaml')

#load survey datasets
yrbss = YRBSSDataset.load_dataset('data/yrbss.yaml')

rq.use_connection(Redis())


async def run_task(task, *args, loop=None, **kwargs):
    '''
    Returns job result or None if an error occurs
    '''
    job = task.delay(*args, **kwargs)
    #  while True:
    for i in range(100000):
        print(i, file=sys.stderr)
        await asyncio.sleep(0.01, loop=loop)
        if job.is_finished:
            return job.result
        if job.is_failed:
            raise Exception('Job is failed')


@job('high', connection=redis_conn, timeout=20)
def get_questions(year=None):
    def get_meta(k, v):
        key = k.lower()
        res = dict(meta.qnmeta_dict[key], **v, id=k) if
        key in meta.qnmeta_dict else dict(v, id=k)
        return res
    national = True
    combined = False if year else True
    dset =yrbss.fetch_survey(combined, national, year)
    res = [(k,get_meta(k,v)) for k, v in dset.vars.items()]
    res = OrderedDict(res)
    return jsonify(res)


@job('low', connection=redis_conn, timeout=5)
def add(x, y):
    return x + y

