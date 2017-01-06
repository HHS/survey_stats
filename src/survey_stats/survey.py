import logging
import gc

from collections import namedtuple

import numpy as np
import pandas as pd

import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import ListVector
from rpy2.robjects import Formula
import pandas.rpy.common as com

from parsers import *
from helpr import *

pandas2ri.activate()

rbase = importr('base')
rsvy = importr('survey')
rprll = importr('parallel')
rbase.options(robjects.vectors.ListVector({'mc.cores':rprll.detectCores()}))


#extend Series with fill_none method
# to take care of json/mysql conversion
def fill_none(self):
    return self.where(pd.notnull(self),None)
pd.Series.fill_none = fill_none


def guard_nan(val):
    return None if np.isnan(val) else val


def subset_survey(des, filt):
    #filt is a dict with vars as keys and list of acceptable values as levels
    #example from R:
    #  subset(dclus1, sch.wide=="Yes" & comp.imp=="Yes"
    if not len(filt.keys()) > 0:
        #empty filter, return original design object
        return des
    filtered = rbase.Reduce( "&",
        [filter_var_levels(des, k, v) for k,v in filt.items()])
    return rsvy.subset_survey_design(des, filtered)


def fetch_stats(des, qn, response=True, vars=[]):
    DECIMALS = {
        'mean': 4, 'se': 4, 'ci_l': 4, 'ci_u': 4, 'count':0
    }
    def fetch_stats_by(des, qn_f, vars):
        lvl_f = Formula('~%s' % ' + '.join(vars))
        #svyciprop_local =
        merged = pandas2ri.ri2py(rbase.merge(
            svybyci_yrbs(qn_f, lvl_f, des, svyciprop_yrbs),
            rsvy.svyby(qn_f, lvl_f, des, rsvy.unwtd_count, na_rm=True,
                       na_rm_by=True, na_rm_all=True, multicore=True)
        ))
        del merged['se']
        merged.columns = vars + ['mean', 'se', 'ci_l', 'ci_u', 'count']
        merged['level'] = len(vars)
        merged['q'] = qn
        merged['q_resp'] = response
        merged = merged.round(DECIMALS)
        return merged.apply(lambda r: r.fill_none().to_dict(), axis=1)
    # create formula for selected question and risk profile
    # ex: ~qn8, ~!qn8
    qn_f = Formula('~%s%s' % ('' if response else '!', qn))
    count = rbase.as_numeric(rsvy.unwtd_count(qn_f, des, na_rm=True,
                                              multicore=True))[0]
    total_ci = None
    if count > 0:
        total_ci = svyciprop_yrbs(qn_f, des, multicore=True)
    #extract stats
    res = { 'level': 0,
           'mean': guard_nan(
               rbase.as_numeric(total_ci)[0]) if total_ci else None,
           'se': guard_nan(
               rsvy.SE(total_ci)[0]) if total_ci else None,
           'ci_l': guard_nan(
               rbase.attr(total_ci,'ci')[0]) if total_ci else None,
           'ci_u': guard_nan(
               rbase.attr(total_ci,'ci')[1]) if total_ci else None,
           'count': count }
    #round as appropriate
    res = {k: round(v, DECIMALS[k]) if k in DECIMALS else v for k,v in
           res.items()}
    #setup the result list
    res = [res]
    vstack = vars[:]
    while len(vstack) > 0:
        #get stats for each level of interactions in vars
        #using svyby to compute across combinations of loadings
        res.extend(fetch_stats_by(des, qn_f, vstack))
        vstack.pop()
    return res


class AnnotatedSurvey(namedtuple('AnnotatedSurvey', ['vars','des', 'rdf'])):
    __slots__ = ()

    @property
    def sample_size(self):
        subs = self.des
        return rbase.dim(subs[subs.names.index('variables')])[0]

    def subset(self, filter):
        return self._replace(des=subset_survey_design(self.des, filter))


    def fetch_stats(self, qn, response=True, vars=[]):
        return fetch_stats(qn, response, vars)


    @classmethod
    def load_cdc_survey(cls, spss_file, dat_files):
        logging.info('loading column definitions')
        svy_cols = parse_fwfcols_spss(spss_file)

        logging.info('loading variable annotations')
        svy_vars = parse_surveyvars_spss(spss_file)

        logging.info('loading survey data from fixed-width file')
        rdf = load_survey(dat_files, svy_cols, svy_vars)

        logging.info('creating survey design from data and annotations')
        des = rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
                             strata=Formula('~stratum'), data=rdf, nest=True)
        return cls(des=des, vars=svy_vars, rdf=rdf)


    @classmethod
    def from_rdf(cls, spss_file, rdf):
        logging.info('loading column definitions')
        svy_cols = parse_fwfcols_spss(spss_file)

        logging.info('loading variable annotations')
        svy_vars = parse_surveyvars_spss(spss_file)

        logging.info('creating survey design from data and annotations')
        des = rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
                             strata=Formula('~stratum'), data=rdf, nest=True)
        return cls(des=des, vars=svy_vars, rdf=rdf)


