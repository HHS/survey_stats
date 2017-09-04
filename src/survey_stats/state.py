from survey_stats.datasets import SurveyDataset
from survey_stats import log
import blaze as bz
import sqlalchemy as sa

lgr = log.getLogger(__name__)


meta = {}
dset = {}


url = 'monetdb://monetdb:monetdb@localhost/survey'
ngin = sa.create_engine(url)
dbc = bz.data(ngin)
lgr.info('was summoned into being, loading up some data', dbc=dbc)

dset['brfss'] = SurveyDataset.load_dataset('config/data/brfss.yaml', dbc)
