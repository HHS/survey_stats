import os
import io
import zipfile
import pandas as pd
import urllib.request
import multiprocessing
from retry import retry
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from botocore.vendored import requests
#import requests_cache
import pandas as pd

from survey_stats import log

import dask
from dask import dataframe as dd
from dask.distributed import Executor
from dask.delayed import delayed

MAX_SOCRATA_FETCH=2**32
TMP_API_KEY='Knx7W1eldgzkO9nUXNYfGXGBJ'
#TODO: move to Vault/elsewhere


#requests_cache.install_cache()
logger = log.getLogger(__name__)
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

def fetch_s3_bytes(url):
    bucket, key = url[5:].split('/', 1)
    logger.info('fetching s3 url', url=url, bucket=bucket, key=key)
    obj = s3.get_object(Bucket=bucket, Key=key)
    return obj['Body']

@retry(tries=5, delay=2, backoff=2, logger=logger)
def fetch_data_from_url(url):
    if os.path.isfile(url):
        return open(url,'r',errors='ignore')
    elif url.startswith('s3://'):
        return fetch_s3_bytes(url)
    else:
        return urllib.request.urlopen(url)

def request_from_socrata_url(url):
    url = url + "$limit=%d" % (MAX_SOCRATA_FETCH)
    r = requests.get(url, headers={'Accept': 'application/json', 'X-App-Token':TMP_API_KEY})
    logger.info("fetching df from url", url=url)
    return r
