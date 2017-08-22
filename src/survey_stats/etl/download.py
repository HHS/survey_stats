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
from boto3.s3transfer import TransferConfig
from botocore.vendored import requests
#import requests_cache
import pandas as pd
import tempfile
from survey_stats import log


MAX_SOCRATA_FETCH=2**32
TMP_API_KEY='Knx7W1eldgzkO9nUXNYfGXGBJ'
#TODO: move to Vault/elsewhere

KB = 1024
MB = KB * KB

#requests_cache.install_cache()
logger = log.getLogger(__name__)
_s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
tcfg = TransferConfig(max_concurrency=4, multipart_chunksize=64*MB)
def fetch_s3_bytes(url):
    bucket, key = url[5:].split('/', 1)
    logger.info('fetching s3 url', url=url, bucket=bucket, key=key)
    obj = _s3.get_object(Bucket=bucket, Key=key)
    return obj['Body']

def fetch_s3_file(url):
    bucket, key = url[5:].split('/', 1)
    logger.info('fetching s3 file', url=url, bucket=bucket, key=key)
    bucket = s3.Bucket(bucket)
    obj = bucket.Object(key)
    with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as tempf:
        obj.download_fileobj(tempf, Config=tcfg)
        tempf.close()
    return fetch_data_from_url(tempf.name)

#@retry(tries=5, delay=2, backoff=2, logger=logger)
def fetch_data_from_url(url):
    if os.path.isfile(url):
        return open(url,'rb')
    elif url.startswith('s3://'):
        return fetch_s3_file(url)
    else:
        return urllib.request.urlopen(url)


def df_from_socrata_url(url):
    url = url + "&$limit=%d" % (MAX_SOCRATA_FETCH)
    r = requests.get(url, headers={'Accept': 'application/json', 'X-App-Token':TMP_API_KEY})
    data = pd.DataFrame(r.json())
    return data
