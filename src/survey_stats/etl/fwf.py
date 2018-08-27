import pandas as pd
import logging
from collections import OrderedDict
from survey_stats import helpr
from survey_stats import log


logger = log.getLogger(__name__)


def load_survey_data(dat_files, svy_cols):
    logger.info('parsing raw survey data: %s' % ','.join(dat_files))
    df = pd.concat(map(lambda dat_f: pd.read_fwf(dat_f,
                                                 colspecs=list(svy_cols.values()),
                                                 names=list(svy_cols.keys()),
                                                 na_values=['.','']),
                       dat_files), ignore_index=True, copy=False)

