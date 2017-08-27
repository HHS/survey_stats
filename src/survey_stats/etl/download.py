import os
import io
import pandas as pd
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from boto3.s3.transfer import TransferConfig
from botocore.vendored import requests
import requests_cache
from survey_stats import log

SCRATCH_DIR = 'cache/'
MAX_SOCRATA_FETCH = 2**32
TMP_API_KEY = 'Knx7W1eldgzkO9nUXNYfGXGBJ'
# TODO: move to Vault/elsewhere

KB = 1024
MB = KB * KB

requests_cache.install_cache()
logger = log.getLogger(__name__)
_s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
tcfg = TransferConfig(max_concurrency=4, multipart_chunksize=256*MB,
                      max_io_queue=1000000, io_chunksize=64*MB)


def fetch_s3_bytes(url):
    bucket, key = url[5:].split('/', 1)
    logger.info('fetching s3 url', url=url, bucket=bucket, key=key)
    obj = _s3.get_object(Bucket=bucket, Key=key)
    return obj['Body']


def fetch_s3_file(url):
    bucket, key = url[5:].split('/', 1)
    logger.info('fetching s3 file', url=url, bucket=bucket, key=key)
    cf = SCRATCH_DIR + key
    if os.path.isfile(cf):
        return fetch_data_from_url(cf)
    try:
        os.makedirs(os.path.dirname(cf))
    except:
        pass
    tempf = open(cf, 'wb')
    obj = s3.Bucket(bucket).Object(key)
    obj.download_fileobj(tempf, Config=tcfg)
    tempf.close()
    return fetch_data_from_url(cf)


def fetch_url(url):
    r = requests.get(url)
    tempf = io.BytesIO(r.content)
    tempf.seek(0)
    return tempf


#  @retry(tries=5, delay=2, backoff=2, logger=logger)
def fetch_data_from_url(url):
    if os.path.isfile(url):
        return open(url, 'rb')
    elif url.startswith('s3://'):
        return fetch_s3_file(url)
    else:
        return fetch_url(url)


def df_from_socrata_url(url):
    url = url + "&$limit=%d" % (MAX_SOCRATA_FETCH)
    r = requests.get(url, headers={'Accept': 'application/json',
                                   'X-App-Token': TMP_API_KEY})
    data = pd.DataFrame(r.json())
    return data
