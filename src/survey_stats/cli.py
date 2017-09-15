import click
import functools
import survey_stats
from survey_stats.dbi import DatabaseConfig, DatabaseType
from survey_stats import api
from survey_stats import microservice
from survey_stats.const import *
from survey_stats import log

logger = log.getLogger('cli')


def resolve_db_args(db_host, db_port, db_type,
                    db_user, db_password, db_name, db_config):
    db_type = DatabaseType(db_type)
    dbc = DatabaseConfig(host=db_host, port=db_port,
                         type=DatabaseType(db_type), user=db_user,
                         password=db_password, name=db_name)
    if db_config:
        dbc = DatabaseConfig.from_yaml(db_config)
    return dbc


database_params = [
    click.option('-c', '--cache-dir', type=CLICK_DIR_PATH,
                 default=DEFAULT_CACHE_DIR,
                 help='directory with data files default:cache'),
    click.option('-C', '--db-config', type=CLICK_FILE_PATH,
                 help='database config yaml, takes priority'),
    click.option('-H', '--db-host', type=click.STRING,
                 envvar='SVY_DBHOST', default='localhost',
                 help='hostname/ip for database'),
    click.option('-P', '--db-port', type=CLICK_TCP_PORT,
                 envvar='SVY_DBPORT', default=50000,
                 help='database host port'),
    click.option('-T', '--db-type', type=click.Choice([t.value for t in DatabaseType]),
                 envvar='SVY_DBTYPE', default='monetdb',
                 help='host database ip:port or sqlalchemy uri'),
    click.option('-U', '--db-user', type=click.STRING, envvar='SVY_DBUSER',
                 default='monetdb', help='database user, default: monetdb'),
    click.option('-p', '--db-password', envvar='SVY_DBPASSWORD', prompt=True,
                 hide_input=True, default='monetdb', type=click.STRING,
                 help='database password, default: monetdb'),
    click.option('-D', '--db-name', type=click.STRING, envvar='SVY_DBNAME',
                 default='survey', help='database name, default: survey')
]

gunicorn_params = [ 
    click.option('-w', '--workers', type=CLICK_NUM_WORKERS,
                 default=DEFAULT_NUM_WORKERS,
                 envvar='WEB_CONCURRENCY',
                 help='number of workers for server, ' +
                      'default: %d' % DEFAULT_NUM_WORKERS),
    click.option('-x', '--threads', type=CLICK_NUM_THREADS,
                 default=DEFAULT_NUM_THREADS,
                 envvar='GUNICORN_WORKER_THREADS',
                 help='number of threads/worker for server, ' +
                      'default: %d' % DEFAULT_NUM_WORKERS),
    click.option('-u', '--timeout', type=CLICK_TIMEOUT,
                 default=DEFAULT_REQ_TIMEOUT,
                 envvar='GUNICORN_TIMEOUT',
                 help='gunicorn worker timeout in seconds, ' +
                      'default: %d' % DEFAULT_REQ_TIMEOUT),
    click.option('--max-requests', type=int,
                 default=DEFAULT_MAX_REQUESTS,
                 envvar='GUNICORN_MAX_REQUESTS',
                 help='requests/worker before respawn, ' +
                      'default: %d' % DEFAULT_MAX_REQUESTS),
    click.option('--max-requests-jitter', type=click.INT,
                 default=DEFAULT_MAX_REQUESTS_JITTER,
                 envvar='GUNICORN_MAX_JITTER',
                 help='max jitter to add to max requests, ' +
                      'default: %d' % DEFAULT_MAX_REQUESTS_JITTER),
    click.option('-n', '--worker-connections', type=click.INT,
                 default=DEFAULT_MAX_WORKER_CONNS,
                 envvar='GUNICORN_WORKER_CONNECTIONS',
                 help='gunicorn max worker connections, ' +
                      'default: %d' % DEFAULT_MAX_WORKER_CONNS),
    click.option('--debug', type=click.BOOL, default=False,
                 help='turn on debug mode, default: False')
]

def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

@click.group()
def cli():
    click.echo('survey_stats %s' % survey_stats.__version__)


@add_options(database_params+gunicorn_params)
@click.option('-h', '--host', envvar='SVY_SERVER_HOST',
              default=DEFAULT_SVY_API_HOST,
              help='interface to bind API service, default: 0.0.0.0')
@click.option('-p', '--port', type=int, envvar='SVY_SERVER_PORT',
              default=DEFAULT_SVY_API_PORT,
              help='port for API service, default: 7777')
@click.option('-d', '--data-url', type=int, envvar='SVY_DATA_URL',
              help='data archive url for source data files')
@click.option('-u', '--sanic-timeout', type=int,
              default=60, envvar='SANIC_REQUEST_TIMEOUT',
              help='sanic request timeout in seconds, default: 60')
@click.option('-W', '--stats-worker', type=str,
              default='http://localhost:7788',
              help='stats worker uri, default: http://localhost:7788')
@cli.command()
def serve(cache_dir, db_config, db_host, db_port, db_type, db_user, db_password, db_name, workers, threads, timeout, max_requests, max_requests_jitter, worker_connections, debug, stats_worker, sanic_timeout, data_url, port, host):
    from survey_stats.server import APIServer
    from survey_stats.api import setup_app

    options = {
        'bind': '%s:%s' % (host, str(port)),
        'worker_class': 'sanic.worker.GunicornWorker',
        'workers': workers,
        'max_requests': max_requests,
        'max_requests_jitter': max_requests_jitter,
        'worker_connections': worker_connections,
        'timeout': timeout,
        'debug': debug
    }

    api = setup_app(
        dbc=resolve_db_args(db_host, db_port, db_type, db_user,
                            db_password, db_name, db_config),
        cache_dir=cache_dir,
        stats_svc=stats_worker,
        sanic_timeout=sanic_timeout)
    APIServer(api, options).run()

@add_options(database_params+gunicorn_params)
@click.option('-h', '--host', envvar='SVY_WORKER_HOST',
              default=DEFAULT_SVY_WORKER_HOST,
              help='interface to bind work service, default: 0.0.0.0')
@click.option('-p', '--port', type=int, envvar='SVY_WORKER_PORT',
              default=DEFAULT_SVY_WORKER_PORT,
              help='port for worker service, default: 7788')
@cli.command()
def work(cache_dir, db_config, db_host, db_port, db_type, db_user, db_password, db_name, workers, threads, timeout, max_requests, max_requests_jitter, worker_connections, debug, port, host): 
    from survey_stats.server import APIServer
    from survey_stats.microservice import setup_app

    options = {
        'bind': '%s:%s' % (host, str(port)),
        'worker_class': 'gevent',
        'workers': workers,
        'max_requests': max_requests,
        'max_requests_jitter': max_requests_jitter,
        'worker_connections': worker_connections,
        'timeout': timeout,
        'debug': debug
    }
    app = setup_app(
        dbc=resolve_db_args(db_host, db_port, db_type, db_user,
                            db_password, db_name, db_config),
        cache=cache_dir)
    APIServer(app, options).run()


def main(args=None):
    cli()
