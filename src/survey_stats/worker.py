import rq
import multiprocessing
from survey_stats import state as st
from survey_stats.tasks import run_task, task_fetch_slice_stats
from survey_stats import logging


def launch_worker(self, *args, **options):
    try:
        # Instantiate a worker
        worker_class = rq.Worker
        #qs = list(map(rq.Queue, ['high', 'normal', 'low']))
        qs = [rq.Queue('low', async=False)]
        #queues = get_queues(*args, queue_class=import_attribute(options['queue_class']))
        w = worker_class(
            qs,
            connection=qs[0].connection
        )

        # Call use_connection to push the redis connection into LocalStack
        # without this, jobs using RQ's get_current_job() will fail
        rq.use_connection(w.connection)
        w.work(burst=options.get('burst', False))
    except ConnectionError as e:
        print(e)
        sys.exit(1)
