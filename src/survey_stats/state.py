from survey_stats.datasets import SurveyDataset
from survey_stats import log
import os
import blaze as bz
import sqlalchemy as sa
import tarfile as tf
from survey_stats.etl.load import restore_data

lgr = log.getLogger(__name__)

def_url = 'monetdb://monetdb:monetdb@localhost/survey'
dburl = os.getenv('DBURL', def_url)

if not os.path.isfile('.cache.lock'):
    # need to download data and setup db
    data_f = "https://s3.amazonaws.com/cdc-survey-data/cache-04Sep2017.tgz"
    dat = tf.open(data_f, mode='r:gz')
    dat.extractall()
    lgr.info('extracted data cache, now setting up dbs')
    restore_data(dburl)

meta = {}
dset = {}

ngin = sa.create_engine(dburl)
dbc = bz.data(ngin)
lgr.info('was summoned into being, loading up some data', dbc=dbc)

dset['brfss'] = SurveyDataset.load_dataset('config/data/brfss.yaml', dbc)
