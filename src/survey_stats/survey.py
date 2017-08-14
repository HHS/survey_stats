import pandas as pd
from cytoolz.functoolz import thread_first, thread_last
from cytoolz.itertoolz import concat
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
from survey_stats.helpr import svyciprop_yrbs, svybyci_yrbs, subset_des_wexpr
from survey_stats.helpr import filter_survey_var
from survey_stats import pdutil as u
from survey_stats import log

rbase = importr('base')
rstats = importr('stats')
rsvy = importr('survey')
rfeather = importr('feather')

DECIMALS = {
    'mean': 4,
    'se': 4,
    'ci_l': 4,
    'ci_u': 4,
    'count': 0
}

logger = log.getLogger()


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


def fetch_stats_by(des, qn_f, vars):
    lvl_f = Formula('~%s' % ' + '.join(vars))
    df = pandas2ri.ri2py(rbase.merge(
        svybyci_yrbs(qn_f, lvl_f, des, svyciprop_yrbs),
        rsvy.svyby(qn_f, lvl_f, des, rsvy.unwtd_count, na_rm=True,
                   na_rm_by=True, na_rm_all=True, multicore=False)
    )).round(DECIMALS)
    df.columns = vars + ['mean', 'se', 'ci_l', 'ci_u', 'count']


def fetch_stats(des, qn, vars=[], filt={}):
    # ex: ~qn8
    qn_f = Formula('~%s' % (qn))
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
        res.extend(fetch_stats_by(des, qn_f, vstack)
                   .assign(level=len(vars),
                           q=qn))
        vstack.pop()

    return res


def sample_size(d):
    return rbase.dim(d[d.names.index('variables')])[0]

def subset(d, filter):
    return d._replace(des=subset_survey(d, filter))

def generate_slices(d, qn, vars=[], filt={}):
    # create the overall filter
    filt_fmla = u.fmla_for_filt(filt)
    # subset the rdf as necessary
    subs = subset_des_wexpr(d, filt_fmla) if len(
        filt) > 0 else d
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
    # setup the formula based on the qn
    # add the base case with empty slice filter
    #   and dicts of qn/resp fmla, slice selector fmla, filt fmla
    res = [{'q': qn, 'f': filt, 's': s} for s in [{}, *calls]]
    logger.info(res)
    return res

def fetch_stats_for_slice(d, q, r, f, s, cfg):
    # create formula for selected question and risk profile
    # create the overall filter
    nat_f = '(' + u.fmla_for_slice(cfg['national_selector']) + ')'
    #not national if sitecode in filters or vars
    # otherwise national
    nat_keys = set(cfg['national_selector'].keys())
    if nat_keys.issubset(f.keys()) or nat_keys.issubset(s.keys()):
        nat_f = '!' + nat_f
    filt_f = u.fmla_for_filt(f) if len(f.keys()) > 0 else ''
    slice_f = u.fmla_for_slice(s) if len(s.keys()) > 0 else ''
    qn_f = Formula('~%s%s' % ('', q))
    subs_f = (filt_f + ' & ' + slice_f
              if len(filt_f) > 0 and len(slice_f) > 0
              else filt_f + slice_f)
    subs_f += ' & ' + nat_f if len(subs_f) > 0 else nat_f
    logger.info("FORMULA: %s" % subs_f)
    # subset the design using the slice fmla
    des = subset_des_wexpr(d, subs_f) if len(
        subs_f) > 0 else d
    count = rbase.as_numeric(rsvy.unwtd_count(qn_f, des, na_rm=True,
                                              multicore=False))[0]
    logger.info("FORMULA: %s, %s, %d" % (q, subs_f, count))
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
        'response': bool(r),
        'q': q}
    res.update(s)
    # round as appropriate
    res = {k: round(v, DECIMALS[k]) if k in DECIMALS and v != None else v for k, v in
           res.items()}
    rbase.gc()
    return res



def des_from_feather(cls, fthr_file):
    rdf = rfeather.read_feather(fthr_file)
    logger.info('creating survey design from data and annotations')
    return rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
                         strata=Formula('~strata'), data=rdf, nest=True)


def des_from_survey_db(cls, svydb):
    return rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
                         strata=Formula('~strata'), nest=True,
                         data=svydb['table'], dbname=svydb[''])

