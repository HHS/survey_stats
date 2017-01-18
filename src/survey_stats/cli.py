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
import argparse
from survey_stats.server import APIServer, number_of_workers
from survey_stats.api import app as api

parser = argparse.ArgumentParser(description='Unified Survey Stats Repository')
subparsers = parser.add_subparsers()

parser_serve = subparsers.add_parser('serve')
parser_serve.add_argument('--host',
                          default = os.environ.get('HOST', '0.0.0.0'),
                          help = 'interface to bind API service, default: 0.0.0.0')
parser_serve.add_argument('--port', type=int,
                          default = os.environ.get('PORT', 7777),
                          help = 'port for API service, default: 7777')
parser_serve.add_argument('--workers', type=int,
                          default = number_of_workers(),
                          help = 'number of worker processes, default: num_cores/2')
parser_serve.add_argument('--max-requests', type=int,
                          default = 1,
                          help = 'requests to serve per worker before respawn, default: 1')
parser_serve.add_argument('--max-requests-jitter', type=int,
                          default = 3,
                          help = 'max jitter to add to max requests, default: 3')

def default_action(args):
    parser.print_help()

def serve_api(args):
    options = {
        'bind': '%s:%s' % (args.host, str(args.port)),
        'workers': args.workers,
        'max_requests': args.max_requests,
        'max_requests_jitter': args.max_requests_jitter,
        'when_ready': boot_when_ready
    }
    APIServer(api, options).run()

parser_serve.set_defaults(func=serve_api)
parser.set_defaults(func=default_action)

def main(args=None):
    args = parser.parse_args(args=args)
    args.func(args)
