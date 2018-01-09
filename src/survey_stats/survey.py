import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
from rpy2 import robjects as ro
from survey_stats.helpr import svyciprop_xlogit, svybyci_xlogit, factor_summary
from survey_stats.helpr import filter_survey_var, rm_nan_survey_var, svyby_nodrop
from survey_stats.helpr import fix_lonely_psus
from survey_stats import pdutil as u
from survey_stats.const import DECIMALS
from survey_stats import log
import gc

rbase = importr('base')
rstats = importr('stats')
rsvy = importr('survey')

rfeather = importr('feather', on_conflict='warn')
rmonet = importr('MonetDB.R')

logger = log.getLogger()


def dim_design(d):
    return pandas2ri.ri2py(rbase.dim(d[d.names.index('variables')]))

def subset_survey(des, filt, qn=None):
    # filt is a dict with vars as keys and list of acceptable values as levels
    # example from R:
    #  subset(dclus1, sch.wide=="Yes" & comp.imp=="Yes"
    if not len(filt.keys()) > 0:
        # empty filter, return original design object
        return des
    filtered = rbase.Reduce(
        "&",
        [filter_survey_var(des, k, v) for k, v in filt.items()] +
        ([rm_nan_survey_var(des, qn)] if qn else [])
    )
    return rsvy.subset_survey_design(des, filtered)


def fetch_stats_by(des, qn_f, r, vs):
    lvl_f = '~%s' % '+'.join(vs)
    ct_f = '%s + %s' % (lvl_f, qn_f[1:])
    logger.info('gen stats for interaction level', lvl_f=lvl_f, qn_f=qn_f, ct_f=ct_f, r=r)
    cols = vs + ['mean', 'se', 'ci_l', 'ci_u']
    df = svybyci_xlogit(Formula(qn_f), Formula(lvl_f), des, svyciprop_xlogit, vartype=['se', 'ci']) 
    df = pandas2ri.ri2py(df)
    df.columns = cols
    df = df.set_index(vs)
    cts = svyby_nodrop(Formula(lvl_f), Formula(ct_f), des, rsvy.unwtd_count, keep_var=True)
    cts = pandas2ri.ri2py(cts).fillna(0.0)
    cts.columns = vs + ['eql', 'ct', 'se_ignore']
    cts = cts.set_index(vs)
    cts['eql'] = cts.eql.apply(lambda x: x == 'TRUE' if type(x) == str else x > 0)
    counts = cts.ct[cts.eql == True].tolist()
    ssizes = cts.groupby(vs).sum()['ct']
    df = df.assign(count=counts, sample_size=ssizes)
    if df.shape[0] > 0:
        df['response'] = r
        df['level'] = len(vs)
    rdf = u.fill_none(df.round(DECIMALS)).reset_index()
    logger.info('create svyby df', df=rdf, vars=vs, eq=cts)
    return rdf


def fetch_stats_totals(des, qn_f, r):
    total_ci = svyciprop_xlogit(Formula(qn_f), des, multicore=False)
    # extract stats
    logger.info('fetching stats totals', r=r, q=qn_f)
    cts = rsvy.svyby(Formula(qn_f), Formula(qn_f), des,
                     rsvy.unwtd_count, na_rm=True,
                     na_rm_by=True, na_rm_all=True, multicore=False)
    cts = pandas2ri.ri2py(cts)
    cols = ['eql', 'ct', 'se_ignore']
    cts.columns = cols
    ct = cts.ct[cts.eql == 1].sum()
    ss = cts.ct.sum()
    res = {'level': 0,
           'response': r,
           'mean': u.guard_nan(
               rbase.as_numeric(total_ci)[0]) if total_ci else None,
           'se': u.guard_nan(
               rsvy.SE(total_ci)[0]) if total_ci else None,
           'ci_l': u.guard_nan(
               rbase.attr(total_ci, 'ci')[0]) if total_ci else None,
           'ci_u': u.guard_nan(
               rbase.attr(total_ci, 'ci')[1]) if total_ci else None,
           'count': ct,
           'sample_size': ss
           }
    # round as appropriate
    logger.info('finished computation lvl1', res=res,
                total_ci=total_ci, ct=ct, ss=ss)
    res = pd.DataFrame([res]).round(DECIMALS)
    return u.fill_none(res)


def fetch_stats(des, qn, r, vs=[], filt={}):
    # ex: ~qn8
    rbase.gc()
    gc.collect()
    qn_f = '~I(%s=="%s")' % (qn, r)
    logger.info('subsetting des with filter', filt=filt)
    des = subset_survey(des, filt)
    logger.info('done subsetting')
    dfs = [fetch_stats_totals(des, qn_f, r)]
    levels = [vs[:k+1] for k in range(len(vs))]
    sts = map(lambda lvl: fetch_stats_by(des, qn_f, r, lvl), levels)
    dfz = pd.concat(dfs + sts, ignore_index=True)
    # get stats_by_fnats for each level of interactions in vars
    # using svyby to compute across combinations of loadings
    logger.info('finished computations, appending dfs', dfs=dfz)
    return u.fill_none(dfz)  # .round(DECIMALS)


def subset(d, filter):
    return d._replace(des=subset_survey(d, filter))


def des_from_feather(fthr_file, denovo=False, fpc=False):
    rbase.gc()
    gc.collect()
    fix_lonely_psus()
    rdf = rfeather.read_feather(fthr_file)
    logger.info('creating survey design from data and annotations',
                cols=list(rbase.colnames(rdf)))
    strata = '~strata'
    if denovo:
        strata = '~year+strata'
    res = rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
                         strata=Formula(strata), data=rdf, nest=True,
                         fpc=(Formula('~fpc') if fpc else ro.NULL))
    rbase.gc()
    gc.collect()
    return res


def des_from_survey_db(tbl, db, host, port, denovo=False, fpc=False):
    strata = '~strata'
    if denovo:
        strata = '~yr+sitecode'
    return rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
                          strata=Formula(strata), nest=True,
                          fpc=(Formula('~fpc') if fpc else ro.NULL),
                          data=tbl, dbname=db, host=host, port=port,
                          dbtype='MonetDB.R')

