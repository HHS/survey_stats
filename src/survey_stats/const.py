from multiprocessing import cpu_count
import click

KB = 1024
MB = KB * KB

DECIMALS = {
    'mean': 6,
    'se': 4,
    'ci_l': 6,
    'ci_u': 6,
    'sample_size': 0,
    'count': 0
}

ID_COLUMN = 'qid'
ANNO_COLUMNS = ['qid', 'response', 'sitecode', 'year']
STATS_COLUMNS = ['mean', 'ci_u', 'ci_l', 'se', 'count', 'sample_size']

DBURI_FMT = '{dbtype}://{user}:{password}@{host}:{port}/{dbname}'
DBTBL_FMT = '{dsid}_{part}'
DSFILE_FMT = '{dsid}_{part}.{type}'

DEFAULT_CACHE_DIR = 'cache'
DEFAULT_SVY_API_HOST = '0.0.0.0'
DEFAULT_SVY_API_PORT = 7777
DEFAULT_SVY_WORKER_HOST = '0.0.0.0'
DEFAULT_SVY_WORKER_PORT = 7788

DEFUALT_CACHE_DIR = 'cache'
DEFAULT_NUM_WORKERS = int(cpu_count() * 1.0)
DEFAULT_NUM_THREADS = int(cpu_count() * 0.0)
DEFAULT_MAX_WORKER_CONNS = 1024
DEFAULT_REQ_TIMEOUT = 180
DEFAULT_MAX_REQUESTS = 0
DEFAULT_MAX_REQUESTS_JITTER = 0

MAX_NUM_WORKERS = int(cpu_count() * 4.0)  # try to keep this sane for platform
MAX_NUM_THREADS = int(cpu_count() * 0.0)  # try to keep this sane
MAX_REQ_TIMEOUT = 60 * 10  # ten minutes is a long time for a req to return
MAX_CONCURRENT_REQ = int(cpu_count() - 1)

CLICK_TCP_PORT = click.IntRange(min=1, max=2**16-1, clamp=False)
CLICK_DIR_PATH = click.Path(exists=True, file_okay=False)
CLICK_FILE_PATH = click.Path(exists=True, dir_okay=False)
CLICK_NUM_WORKERS = click.IntRange(min=1, max=MAX_NUM_WORKERS, clamp=True)
CLICK_NUM_THREADS = click.IntRange(min=1, max=MAX_NUM_THREADS, clamp=True)
CLICK_TIMEOUT = click.IntRange(min=1, max=60*10, clamp=True)

DEFAULT_SANIC_RESPONSE_TIMEOUT = 600 #Default max Sanic response timeout
DEFAULT_HTTP_RESPONSE_TIMEOUT = 600 #Default max Sanic response timeout
