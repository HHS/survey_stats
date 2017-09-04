"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

You might be tempted to import things from __main__ later, but that will cause
problems: the code will get executed twice:

- When you run `python -msurvey_stats` python will execute
``__main__.py`` as a script. That means there won't be any
``survey_stats.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
there's no ``survey_stats.__main__`` in ``sys.modules``.

Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import os
import yaml
import argparse
import multiprocessing
from survey_stats import log
import tarfile as tf
from survey_stats.etl.load import restore_data
import urllib.request

logger = log.getLogger('cli')

DEFAULT_NUM_WORKERS = int(multiprocessing.cpu_count() / 2.0)

parser = argparse.ArgumentParser(description='Unified Survey Stats Repository')
subparsers = parser.add_subparsers()

parser_serve = subparsers.add_parser('serve')
parser_serve.add_argument('--host', default=os.environ.get('HOST', '0.0.0.0'),
                          help='interface to bind API service, default: 0.0.0.0')
parser_serve.add_argument('--port', type=int, default=os.environ.get('PORT', 7777),
                          help='port for API service, default: 7777')
parser_serve.add_argument('--processes', type=int, default=DEFAULT_NUM_WORKERS,
                          help='number of processes to use for server, default: num_cores/2')
parser_serve.add_argument('--stats_uri', type=str, default='http://localhost:7788',
                          help='stats worker uri, default: http://localhost:7788')
parser_serve.add_argument('--db_conf', type=argparse.FileType('r'),
                          help='database connection info yaml, default: config/db-default.yaml')
parser_serve.add_argument('--debug', action='store_true',
                          help='turn on debug mode, default: False')

parser_prole = subparsers.add_parser('work')
parser_prole.add_argument('--host', default=os.environ.get('HOST', '0.0.0.0'),
						  help='interface to bind API service, default: 0.0.0.0')
parser_prole.add_argument('--port', type=int, default=os.environ.get('PORT', 7788),
        				  help='port for API service, default: 7788')
parser_prole.add_argument('--workers', type=int, default=DEFAULT_NUM_WORKERS,
        				  help='number of worker processes, default: num_cores/2')
parser_prole.add_argument('--db_conf', type=argparse.FileType('r'),
                          help='database connection info yaml, default: config/db-default.yaml')
parser_prole.add_argument('--max-requests', type=int, default=0,
        				  help='requests to prole per worker before respawn, default: 1000')
parser_prole.add_argument('--max-requests-jitter', type=int, default=0,
        				  help='max jitter to add to max requests, default: 3')
parser_prole.add_argument('--debug', action='store_true',
                          help='turn on debug mode, default: False')
parser_prole.add_argument('--timeout', type=int, default=600,
        				  help='worker request timeout in seconds, default: 600')


def default_action(args):
    parser.print_help()


def serve_api(args):
    from survey_stats.server import APIServer
    from survey_stats.api import setup_app
    dbc = args.db_conf if args.db_conf else open('config/db-default.yaml')
    dbconf = yaml.load(dbc)
    dbc.close()
    def_url = 'monetdb://monetdb:monetdb@localhost/survey'
    dburl = os.getenv('DBURL', def_url)

    if not os.path.isfile('.cache.lock'):
        # need to download data and setup db
        data_f = "https://s3.amazonaws.com/cdc-survey-data/cache-04Sep2017.tgz"
        logger.info('fetching data cache', url=data_f)
        urllib.request.urlretrieve(data_f, './cache.tar.gz')
        dat = tf.open('cache.tar.gz', mode='r:gz')
        dat.extractall('.')
        logger.info('extracted data cache, now setting up dbs')
        restore_data(dburl)

    options = {
        'bind': '%s:%s' % (args.host, str(args.port)),
        'db_conf': dbconf,
        'stats_svc': args.stats_uri,
        'worker_class': "sanic.worker.GunicornWorker",
        'workers': args.processes,
        'timeout': 5000,
        'debug': args.debug
        #'when_ready': boot_when_ready
    }
    api = setup_app(
        db_conf=options['db_conf'],
        stats_svc=options['stats_svc'])
    APIServer(api, options).run()


def serve_workers(args):
    from survey_stats.server import APIServer
    from survey_stats.microservice import setup_app
    dbc = args.db_conf if args.db_conf else open('config/db-default.yaml')
    dbconf = yaml.load(dbc)
    dbc.close()
    options = {
        'bind': '%s:%s' % (args.host, str(args.port)),
        'db_conf': dbconf,
        'workers': args.workers,
        'max_requests': args.max_requests,
        'max_requests_jitter': args.max_requests_jitter,
        'debug': args.debug
        #'when_ready': boot_when_ready
    }
    app = setup_app(db_conf=options['db_conf'])
    APIServer(app, options).run()


parser_serve.set_defaults(func=serve_api)
parser_prole.set_defaults(func=serve_workers)
parser.set_defaults(func=default_action)


def main(args=None):
    args = parser.parse_args(args=args)
    args.func(args)
