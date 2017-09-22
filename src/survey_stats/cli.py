import click
import survey_stats
from survey_stats.dbi import DatabaseConfig, DatabaseType
import survey_stats.const as c
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
    click.option('-c', '--cache-dir', type=c.CLICK_DIR_PATH,
                 default=c.DEFAULT_CACHE_DIR,
                 help='directory with data files default:cache'),
    click.option('-C', '--db-config', type=c.CLICK_FILE_PATH,
                 help='database config yaml, takes priority'),
    click.option('-H', '--db-host', type=click.STRING,
                 envvar='SVY_DBHOST', default='localhost',
                 help='hostname/ip for database'),
    click.option('-P', '--db-port', type=c.CLICK_TCP_PORT,
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
                 default='survey', help='database name, default: survey'),
    click.option('-F', '--feather', is_flag=True,
                 help='use feather (in-memory) instead of db')
]

gunicorn_params = [
    click.option('-w', '--workers', type=c.CLICK_NUM_WORKERS,
                 default=c.DEFAULT_NUM_WORKERS,
                 envvar='WEB_CONCURRENCY',
                 help='number of workers for server, ' +
                      'default: %d' % c.DEFAULT_NUM_WORKERS),
    click.option('--threads', type=c.CLICK_NUM_THREADS,
                 default=c.DEFAULT_NUM_THREADS,
                 envvar='GUNICORN_WORKER_THREADS',
                 help='number of threads/worker for server, ' +
                      'default: %d' % c.DEFAULT_NUM_WORKERS),
    click.option('--timeout', type=c.CLICK_TIMEOUT,
                 default=c.DEFAULT_REQ_TIMEOUT,
                 envvar='GUNICORN_TIMEOUT',
                 help='gunicorn worker timeout in seconds, ' +
                      'default: %d' % c.DEFAULT_REQ_TIMEOUT),
    click.option('--max-requests', type=int,
                 default=c.DEFAULT_MAX_REQUESTS,
                 envvar='GUNICORN_MAX_REQUESTS',
                 help='requests/worker before respawn, ' +
                      'default: %d' % c.DEFAULT_MAX_REQUESTS),
    click.option('--max-requests-jitter', type=click.INT,
                 default=c.DEFAULT_MAX_REQUESTS_JITTER,
                 envvar='GUNICORN_MAX_JITTER',
                 help='max jitter to add to max requests, ' +
                      'default: %d' % c.DEFAULT_MAX_REQUESTS_JITTER),
    click.option('-n', '--worker-connections', type=click.INT,
                 default=c.DEFAULT_MAX_WORKER_CONNS,
                 envvar='GUNICORN_WORKER_CONNECTIONS',
                 help='gunicorn max worker connections, ' +
                      'default: %d' % c.DEFAULT_MAX_WORKER_CONNS),
    click.option('--debug', type=click.BOOL, is_flag=True,
                 default=False, help='turn on debug mode, default: False')
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
              default=c.DEFAULT_SVY_API_HOST,
              help='interface to bind API service, default: 0.0.0.0')
@click.option('-p', '--port', type=int, envvar='SVY_SERVER_PORT',
              default=c.DEFAULT_SVY_API_PORT,
              help='port for API service, default: 7777')
@click.option('-s', '--socket', type=str, envvar='SVY_WORKER_SOCKET',
              help='unix socket for worker service')
@click.option('-d', '--data-url', type=int, envvar='SVY_DATA_URL',
              help='data archive url for source data files')
@click.option('--sanic-timeout', type=int,
              default=300, envvar='SANIC_REQUEST_TIMEOUT',
              help='sanic request timeout in seconds, default')
@click.option('-W', '--stats-worker', type=str,
              default='http://localhost:7788',
              help='stats worker uri, default: http://localhost:7788')
@click.option('--stats-socket', type=str,
              default='/tmp/statsworker.sock',
              help='stats worker socket, default: unix:statsworker.sock')
@cli.command()
def serve(cache_dir, db_config, db_host, db_port, db_type, db_user, db_password, db_name, feather, workers, threads, timeout, max_requests, max_requests_jitter, worker_connections, debug, stats_socket, stats_worker, sanic_timeout, data_url, socket, port, host):
    from survey_stats.server import APIServer
    from survey_stats.api import setup_app

    options = {
        'bind': '%s:%s' % (host, str(port)) if not socket else socket,
        'umask': int('007',8),
        'worker_class': 'sanic.worker.GunicornWorker',
        'workers': workers,
        'max_requests': max_requests,
        'max_requests_jitter': max_requests_jitter,
        'worker_connections': worker_connections,
        'timeout': timeout,
        'debug': debug
    }
    logger.info('setting up app', options=options, f=feather)
    app = setup_app(
        dbc=resolve_db_args(db_host, db_port, db_type, db_user,
                            db_password, db_name, db_config),
        cache_dir=cache_dir,
        stats_svc=stats_worker,
        sanic_timeout=sanic_timeout,
        use_feather=feather,
        worker_socket=stats_socket)
    return APIServer(app, options).run()


@add_options(database_params+gunicorn_params)
@click.option('-h', '--host', envvar='SVY_WORKER_HOST',
              default=c.DEFAULT_SVY_WORKER_HOST,
              help='interface to bind work service, default: 0.0.0.0')
@click.option('-p', '--port', type=int, envvar='SVY_WORKER_PORT',
              default=c.DEFAULT_SVY_WORKER_PORT,
              help='port for worker service, default: 7788')
@click.option('-s', '--socket', type=str, envvar='SVY_WORKER_SOCKET',
              help='unix socket for worker service')
@cli.command()
def work(cache_dir, db_config, db_host, db_port, db_type, db_user, db_password, db_name, feather, workers, threads, timeout, max_requests, max_requests_jitter, worker_connections, debug, socket, port, host):
    from survey_stats.server import APIServer
    from survey_stats.microservice import setup_app

    options = {
        'bind': '%s:%s' % (host, str(port)) if not socket else socket,
        'umask': int('007', 8),
        'worker_class': 'sync',
        'workers': workers,
        'max_requests': max_requests,
        'max_requests_jitter': max_requests_jitter,
        'worker_connections': worker_connections,
        'timeout': timeout,
        'debug': debug
    }
    logger.info('setting up app', options=options, f=feather)
    app = setup_app(
        dbc=resolve_db_args(
            db_host, db_port, db_type,
            db_user, db_password, db_name,
            db_config),
        cdir=cache_dir,
        use_feather=feather)
    APIServer(app, options).run()


@add_options(database_params)
@click.option('--parse-all/--no-parse-all', is_flag=True,
              help='parse all datasets')
@click.argument('datasets', type=click.STRING, nargs=-1)
@cli.command()
def parse(cache_dir, db_config, db_host, db_port, db_type, db_user, db_password, db_name, feather, parse_all, datasets):
    import survey_stats.etl.load as l
    l.load_datasets(
        cache_dir=cache_dir,
        dbc=resolve_db_args(
            db_host, db_port, db_type,
            db_user, db_password, db_name,
            db_config),
        dsets=datasets,
        parse_all=parse_all)



def main(args=None):
    cli()
