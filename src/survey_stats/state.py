from survey_stats.datasets import SurveyDataset
from survey_stats import log
import os
import blaze as bz
import sqlalchemy as sa

lgr = log.getLogger(__name__)

meta = {}
dset = {}

def_url = 'monetdb://monetdb:monetdb@localhost/survey'
def_worker_url = 'http://127.0.0.1:7788/'
worker_url = None
dburl = None

def initialize():
    global worker_url, db_url, ngin, dbc, dset
    worker_url = os.getenv('WORKERURL', worker_url)
    dburl = os.getenv('DBURL', def_url)
    ngin = sa.create_engine(dburl)
    dbc = bz.data(ngin)
    lgr.info('was summoned into being, loading up some data', dbc=dbc)
    dset['brfss'] = SurveyDataset.load_dataset('config/data/brfss.yaml', dbc)
