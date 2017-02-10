import logging
import gc
import json
from toolz.itertoolz import concat, concatv, mapcat
from toolz.functoolz import thread_last, thread_first, flip, do, compose
from toolz.curried import map, filter, reduce
from toolz import curry
from collections import namedtuple
from collections import abc
import pandas as pd
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
from survey_stats.parsers import parse_fwfcols_spss, parse_surveyvars_spss
from survey_stats.helpr import svyciprop_yrbs, svybyci_yrbs, subset_des_wexpr
from survey_stats.helpr import filter_survey_var
from survey_stats import pdutil as u

rbase = importr('base')
rstats = importr('stats')
rsvy = importr('survey')

DECIMALS = {
    'mean': 4,
    'se': 4,
    'ci_l': 4,
    'ci_u': 4,
    'count': 0
}


def subset_survey(des, filt):
    # filt is a dict with vars as keys and list of acceptable values as levels
    # example from R:
    #  subset(dclus1, sch.wide=="Yes" & comp.imp=="Yes"
    if not len(filt.keys()) > 0:
        # empty filter, return original design object
        return des
    filtered = rbase.Reduce("&",
                            [filter_survey_var(des, k, v) for k, v in filt.items()])
    return rsvy.subset_survey_design(des, filtered)


def fetch_stats(des, qn, response=True, vars=[], filt={}):
    def fetch_stats_by(des, qn_f, vars):
        lvl_f = Formula('~%s' % ' + '.join(vars))
        # svyciprop_local =
        merged = pandas2ri.ri2py(rbase.merge(
            svybyci_yrbs(qn_f, lvl_f, des, svyciprop_yrbs),
            rsvy.svyby(qn_f, lvl_f, des, rsvy.unwtd_count, na_rm=True,
                       na_rm_by=True, na_rm_all=True, multicore=False)
        ))
        del merged['se']
        merged.columns = vars + ['mean', 'se', 'ci_l', 'ci_u', 'count']
        merged['level'] = len(vars)
        merged['q'] = qn
        merged['q_resp'] = response
        merged = merged.round(DECIMALS)
        #logging.info(merged.to_json(orient='records'))
        return json.loads(merged.to_json(orient='records'))
    # create formula for selected question and risk profile
    # ex: ~qn8, ~!qn8
    qn_f = Formula('~%s%s' % ('' if response else '!', qn))
    count = rbase.as_numeric(rsvy.unwtd_count(qn_f, des, na_rm=True,
                                              multicore=False))[0]
    total_ci = None
    if count > 0:
        total_ci = svyciprop_yrbs(qn_f, des, multicore=False)

    # extract stats
    res = {'level': 0,
           'mean': u.guard_nan(
               rbase.as_numeric(total_ci)[0]) if total_ci else None,
           'se': u.guard_nan(
               rsvy.SE(total_ci)[0]) if total_ci else None,
           'ci_l': u.guard_nan(
               rbase.attr(total_ci, 'ci')[0]) if total_ci else None,
           'ci_u': u.guard_nan(
               rbase.attr(total_ci, 'ci')[1]) if total_ci else None,
           'count': count}
    # round as appropriate
    res = {k: round(v, DECIMALS[k]) if k in DECIMALS else v for k, v in
           res.items()}
    # setup the result list
    res = [res]
    vstack = vars[:]
    while len(vstack) > 0:
        # get stats for each level of interactions in vars
        # using svyby to compute across combinations of loadings
        res.extend(fetch_stats_by(des, qn_f, vstack))
        vstack.pop()

    return res


class AnnotatedSurvey(namedtuple('AnnotatedSurvey', ['vars', 'des', 'rdf'])):
    __slots__ = ()

    @property
    def sample_size(self):
        subs = self.des
        return rbase.dim(subs[subs.names.index('variables')])[0]

    def subset(self, filter):
        return self._replace(des=subset_survey(self.des, filter))

    def generate_slices(self, qn, response, vars=[], filt={}):
        # create the overall filter
        filt_fmla = u.fmla_for_filt(filt)
        # subset the rdf as necessary
        subs = subset_des_wexpr(self.rdf, filt_fmla) if len(
            filt) > 0 else self.rdf
        # create a formula for generating the cross-tabs/breakouts across
        #   the selected vars
        lvl_f = Formula('~%s' % ' + '.join(vars)) if len(vars) > 0 else None
        # generate the crosstab/breakouts for the selected vars,
        #   turn them into R selector expressions and concatenate
        #   each non-empty selector with the R selector for the outer filter
        calls = thread_first(
            rstats.xtabs(lvl_f, subs),
            rbase.as_data_frame,
            pandas2ri.ri2py,
            (pd.DataFrame.query, "Freq > 0"),
            (pd.DataFrame.get, vars),
            lambda df: df.apply(
                lambda z: thread_last(
                    z.to_dict(),
                    lambda y: [(v,y[v]) for v in vars],
                    list,
                    lambda x: [
                        tuple(x[:i + 1]) for
                        i in range(len(x))],
                ), axis=1),
            (pd.DataFrame.to_records, False),
            list,
            concat,
            set,
            map(dict),
            list
        ) if len(vars) > 0 else []
        # setup the formula based on the qn and response
        # add the base case with empty slice filter
        #   and dicts of qn/resp fmla, slice selector fmla, filt fmla
        res = [{'q': qn, 'r': int(response), 'f': filt, 's': s} for s in [{}, *calls]]
        rbase.gc()
        return res

    def fetch_stats_for_slice(self, q, r, f, s):
        # create formula for selected question and risk profile
        # create the overall filter
        filt_f = u.fmla_for_filt(f) if len(f.keys()) > 0 else ''
        slice_f = u.fmla_for_slice(s) if len(s.keys()) > 0 else ''
        qn_f = Formula('~%s%s' % ('' if r else '!', q))
        subs_f = (filt_f + ' & ' + slice_f
                  if len(filt_f) > 0 and len(slice_f) > 0
                  else filt_f + slice_f)
        # subset the design using the slice fmla
        des = subset_des_wexpr(self.des, subs_f) if len(
            subs_f) > 0 else self.des
        count = rbase.as_numeric(rsvy.unwtd_count(qn_f, des, na_rm=True,
                                                  multicore=False))[0]
        total_ci = None
        if count > 0:
            total_ci = svyciprop_yrbs(qn_f, des, multicore=False)

        # extract stats
        res = {'level': slice_f.count('&') + 1 if len(slice_f) > 0 else 0,
               'mean': u.guard_nan(
            rbase.as_numeric(total_ci)[0]) if total_ci else None,
            'se': u.guard_nan(
            rsvy.SE(total_ci)[0]) if total_ci else None,
            'ci_l': u.guard_nan(
            rbase.attr(total_ci, 'ci')[0]) if total_ci else None,
            'ci_u': u.guard_nan(
            rbase.attr(total_ci, 'ci')[1]) if total_ci else None,
            'count': count,
            'filter': f,
            'q_resp': bool(r),
            'q': q}
        res.update(s)
        # round as appropriate
        res = {k: round(v, DECIMALS[k]) if k in DECIMALS and v != None else v for k, v in
               res.items()}
        rbase.gc()
        return res

    def fetch_stats_linear(self, qn, response=True, vars=[], filt={}):
        return fetch_stats(self.des, qn, response, vars, filt)

    def var_in_svy(self, var):
        return self.vars.has_key(var)

    def var_lvl_in_svy(self, var, lvl):
        return self.var_in_svy(var)

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
