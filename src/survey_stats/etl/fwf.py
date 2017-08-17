import pandas as pd
import logging
from collections import OrderedDict

import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

from survey_stats import helpr
from survey_stats import log

rbase = importr('base')

logger = log.getLogger()

def load_survey(dat_files, svy_cols, svy_vars):
    logger.info('parsing raw survey data: %s' % ','.join(dat_files))
    df = pd.concat(map(lambda dat_f: pd.read_fwf(dat_f,
                                                 colspecs=list(svy_cols.values()),
                                                 names=list(svy_cols.keys()),
                                                 na_values=['.','']),
                       dat_files), ignore_index=True, copy=False)
    for q, v in svy_vars.items():
        if v['is_integer']:
            (codes, cats) = zip(*v['responses'])
            idx = rdf.colnames.index(q)
            fac = rdf[idx]
            try:
                fac = rbase.as_integer(fac)
                fac = rbase.factor(fac, levels=list(codes), labels=list(cats))
                rdf[idx] = fac
            except:
                logger.error(rbase.summary(rdf[idx]))
                logger.error(helpr.factor_summary(rdf[idx]))
                logger.error(rbase.summary(fac))
                raise ParseCDCSurveyException('parsing problems: %s -> %s'
                                              % (q, v))
        elif q.startswith('qn'):
            idx = rdf.colnames.index(q)
            fac = rbase.as_integer(rdf[idx])
            coerced = rbase.is_na(fac)
            n_coerced = rbase.sum(coerced)[0]
            if n_coerced > 0:
                coerced = helpr.factor_summary(rdf[idx].rx(coerced))
                logger.warning('Coerced non-numeric values for variable:' +
                                ' %s\n%s' % (q, coerced))
            if rbase.min(fac, na_rm=True)[0] < 1 or \
               rbase.max(fac, na_rm=True)[0] > 2:
                raise ParseCDCSurveyException('Found invalid levels for' +
                                              ' boolean var: %s -> %s' %
                                              (q, helpr.factor_summary(fac)))
            rdf[idx] = helpr.tobool(fac)
    return rdf

def load_survey_py(dat_file, svy_cols, svy_vars):
    df = pd.read_fwf(dat_file, colspecs=list(svy_cols.values()),
                     names=list(svy_cols.keys()), na_values=['.',''])
    logger.info('Parsed raw survey data')
    for q, v in svy_vars.items():
        if v['is_integer']:
            (codes, cats) = zip(*v['responses'])
            try:
                df[q] = pd.Categorical.from_codes(df[q].fillna(-1),
                                                  categories=list(cats),
                                                  ordered=True)
            except:
                logger.error(df[q].describe())
                raise ParseCDCSurveyException('parsing problems: %s -> %s'
                                              % (q, v))
        elif q.startswith('qn'):
            idx = rdf.colnames.index(q)
            fac = rbase.as_integer(rdf[idx])
            coerced = rbase.is_na(fac)
            n_coerced = rbase.sum(coerced)[0]
            if n_coerced > 0:
                coerced = helpr.factor_summary(rdf[idx].rx(coerced))
                logger.warning('Coerced non-numeric values for variable:' +
                                ' %s\n%s' % (q, coerced))
            if rbase.min(fac, na_rm=True)[0] < 1 or \
               rbase.max(fac, na_rm=True)[0] > 2:
                raise ParseCDCSurveyException('Found invalid levels for' +
                                              ' boolean var: %s -> %s' %
                                              (q, helpr.factor_summary(fac)))
    return rdf
