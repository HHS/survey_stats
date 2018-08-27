[![Build Status](https://travis-ci.org/semanticbits/survey_stats.svg?branch=develop)](https://travis-ci.org/semanticbits/survey_stats)
[![Coverage Status](https://coveralls.io/repos/github/semanticbits/survey_stats/badge.svg?branch=develop)](https://coveralls.io/github/semanticbits/survey_stats?branch=develop) 
[![Requirements Status](https://requires.io/github/semanticbits/survey_stats/requirements.svg?branch=develop)](https://requires.io/github/semanticbits/survey_stats/requirements/?branch=develop)


## Overview

Library and webservice for replicating survey statistics for various 
CDC Survey datasets using R and the *survey* package.

## Quickstart

On any Ubuntu 16.04 machine, run:
```
source develop.sh
./bootstrap.sh
```
This will, 
1. install all the required system packages,
2. download and install miniconda in the current user's home directory,
3. setup a conda python virtual environment with the latest Intel Python 3.6.x release,'
4. and install the Python, R, and conda library dependencies specified in `conda_env.yml`
5. install the source as a virtual package into the environment
6. use the bootstrap.sh script to download the latest cache (feather) files containing the survey data, the precomputed data, and related annotations and metadata, and extract it into the `cache/` directory.

Once this is done, in one terminal, start the stats worker with:
```
survey_stats work -F --threads 1 --max-requests 1 -w 3
```
In another, start the stats server with:
```
survey_stats serve -F
```
By default, the worker will be running on all interfaces at port 7788 - `0.0.0.0:7788`, and the server will be running on all interfaces at port 7777 - `0.0.0.0:7777`. Further details about the server and worker CLI arguments are provided below.


#### Worker CLI Arguments
```
  survey_stats work --help                                                       
survey_stats 1.0.0
Usage: survey_stats work [OPTIONS]

Options:
  -p, --port INTEGER              port for worker service, default: 7788
  -h, --host TEXT                 interface to bind work service, default:
                                  0.0.0.0
  --debug                         turn on debug mode, default: False
  -n, --worker-connections INTEGER
                                  gunicorn max worker connections, default:
                                  1024
  --max-requests-jitter INTEGER   max jitter to add to max requests, default:
                                  0
  --max-requests INTEGER          requests/worker before respawn, default: 0
  --timeout INTEGER RANGE         gunicorn worker timeout in seconds, default:
                                  180
  --threads INTEGER RANGE         number of threads/worker for server,
                                  default: 8
  -w, --workers INTEGER RANGE     number of workers for server, default: 8
  -F, --feather                   use feather (in-memory) instead of db
  -D, --db-name TEXT              database name, default: survey
  -p, --db-password TEXT          database password, default: monetdb
  -U, --db-user TEXT              database user, default: monetdb
  -T, --db-type [monetdb|mariadb|mapd]
                                  host database ip:port or sqlalchemy uri
  -P, --db-port INTEGER RANGE     database host port
  -H, --db-host TEXT              hostname/ip for database
  -C, --db-config PATH            database config yaml, takes priority
  -c, --cache-dir DIRECTORY       directory with data files default:cache
  --help                          Show this message and exit.
```

#### Server CLI Arguments
```
  survey_stats serve --help                                                      [14:21:56]
/home/ajish/miniconda/envs/survey_env/lib/python3.6/site-packages/odo/backends/pandas.py:102: FutureWarning: pandas.tslib is deprecated and will be removed in a future version.
You can access NaTType as type(pandas.NaT)
  @convert.register((pd.Timestamp, pd.Timedelta), (pd.tslib.NaTType, type(None)))
survey_stats 1.0.0
Usage: survey_stats serve [OPTIONS]

Options:
  -W, --stats-worker TEXT         stats worker uri, default:
                                  http://localhost:7788
  --sanic-timeout INTEGER         sanic request timeout in seconds, default
  -d, --data-url INTEGER          data archive url for source data files
  -p, --port INTEGER              port for API service, default: 7777
  -h, --host TEXT                 interface to bind API service, default:
                                  0.0.0.0
  --debug                         turn on debug mode, default: False
  -n, --worker-connections INTEGER
                                  gunicorn max worker connections, default:
                                  1024
  --max-requests-jitter INTEGER   max jitter to add to max requests, default:
                                  0
  --max-requests INTEGER          requests/worker before respawn, default: 0
  --timeout INTEGER RANGE         gunicorn worker timeout in seconds, default:
                                  180
  --threads INTEGER RANGE         number of threads/worker for server,
                                  default: 8
  -w, --workers INTEGER RANGE     number of workers for server, default: 8
  -F, --feather                   use feather (in-memory) instead of db
  -D, --db-name TEXT              database name, default: survey
  -p, --db-password TEXT          database password, default: monetdb
  -U, --db-user TEXT              database user, default: monetdb
  -T, --db-type [monetdb|mariadb|mapd]
                                  host database ip:port or sqlalchemy uri
  -P, --db-port INTEGER RANGE     database host port
  -H, --db-host TEXT              hostname/ip for database
  -C, --db-config PATH            database config yaml, takes priority
  -c, --cache-dir DIRECTORY       directory with data files default:cache
  --help                          Show this message and exit.
```

## Deployment

Currently, the build and deployment scripts are only implemented for Ubuntu 16.04 derived distributions. This is due to the fact that specific system libraries that are dependencies loaded by Python, R, and RPy2 need to be installed at the system level. Support for other distributions can be added by explicitly adding support for the distro and mapping the installed system packages in `develop.sh`.

### Production Deployment
The survey stats server Sanic app and worker Flask app are both WSGI/WSGI-compatible implementations that are fronted by a Gunicorn server. For a production system it is important to run the Gunicorn server behind an Nginx reverse proxy, as Gunicorn does not handle slow clients well and does not handle queueing requests very well. Without the Nginx reverse proxy, the chances of a DoS-like scenario remains high even at a low QPS and concurrency. Please see the follow Gunicorn documentation for more details: [http://docs.gunicorn.org/en/stable/deploy.html](http://docs.gunicorn.org/en/stable/deploy.html). Note that this will not preclude worker timeouts when sufficient resources are not available to run the processor and memory intensive advanced query (R survey) computations.
