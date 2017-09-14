from multiprocessing import cpu_count
import click

KB = 1024
MB = KB * KB

DBURI_FMT = '{dbtype}://{user}:{password}@{host}:{port}/{dbname}'
DSFILE_FMT = '{id}_{part}.{type}'

DEFAULT_CACHE_DIR = 'cache'
DEFAULT_SVY_API_HOST = '0.0.0.0'
DEFAULT_SVY_API_PORT = 7777
DEFAULT_SVY_WORKER_HOST = '0.0.0.0'
DEFAULT_SVY_WORKER_PORT = 7788

DEFUALT_CACHE_DIR = 'cache'
DEFAULT_NUM_WORKERS = int(cpu_count() * 2.0)
DEFAULT_NUM_THREADS = int(cpu_count() * 2.0)
DEFAULT_MAX_WORKER_CONNS = 1024
DEFAULT_REQ_TIMEOUT = 60
DEFAULT_MAX_REQUESTS = 0
DEFAULT_MAX_REQUESTS_JITTER = 0

MAX_NUM_WORKERS = int(cpu_count() * 4.0)  # try to keep this sane for platform
MAX_NUM_THREADS = int(cpu_count() * 4.0)  # try to keep this sane
MAX_REQ_TIMEOUT = 60 * 10  # ten minutes is a long time for a req to return

CLICK_TCP_PORT = click.IntRange(min=1, max=2^16-1, clamp=False)
CLICK_DIR_PATH = click.Path(exists=True, file_okay=False)
CLICK_FILE_PATH = click.Path(exists=True, dir_okay=False)
CLICK_NUM_WORKERS = click.IntRange(min=1, max=MAX_NUM_WORKERS, clamp=True)
CLICK_NUM_THREADS = click.IntRange(min=1, max=MAX_NUM_THREADS, clamp=True)
CLICK_TIMEOUT = click.IntRange(min=1, max=60*10, clamp=True)
