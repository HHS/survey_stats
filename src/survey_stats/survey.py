import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
from survey_stats.helpr import svyciprop_yrbs, svybyci_yrbs, factor_summary
from survey_stats.helpr import filter_survey_var
from survey_stats import pdutil as u
from survey_stats.const import DECIMALS
from survey_stats import log
import gc

rbase = importr('base')
rstats = importr('stats')
rpar = importr('parallel')
rsvy = importr('survey')

rfeather = importr('feather', on_conflict='warn')
rmonet = importr('MonetDB.R')

logger = log.getLogger()


def sample_size(d):
    return rbase.dim(d[d.names.index('variables')])

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


def fetch_stats_by(des, qn_f, r, vs):
    rbase.gc()
    gc.collect()
    lvl_f = '~%s' % '+'.join(vs)
    ct_f = '%s + %s' % (lvl_f, qn_f[1:])
    ss = pandas2ri.ri2py(sample_size(des))
    logger.info('gen stats for interaction level', d=ss, lvl_f=lvl_f, qn_f=qn_f, ct_f=ct_f, r=r)
    cols = vs + ['mean', 'se', 'ci_l', 'ci_u']
    df = svybyci_yrbs(Formula(qn_f), Formula(lvl_f), des, svyciprop_yrbs) 
    df = pandas2ri.ri2py(df) if df is not None else pd.DataFrame(
        columns=['level','response']+cols)
    df.columns = cols
    cts = rsvy.svyby(Formula(qn_f), Formula(ct_f), des, rsvy.unwtd_count, na_rm=True,
                     na_rm_by=True, na_rm_all=True, multicore=False)
    cts = pandas2ri.ri2py(cts)
    cols = vs + ['eql', 'ct', 'se_ignore']
    cts.columns = cols
    df = df.reset_index(drop=True).assign(count = cts.ct[cts.eql==1].reset_index(drop=True),
                   sample_size= cts.ct[cts.eql==1].reset_index(drop=True) + cts.ct[cts.eql==0].reset_index(drop=True))
    if df.shape[0] > 0:
        df['response'] = r
        df['level'] = len(vs)
    rdf = u.fill_none(df.round(DECIMALS))
    logger.info('create svyby df', df=rdf, vars=vs, eq=cts.ct[cts.eql==1].reset_index(drop=True))
    return rdf


def fetch_stats_totals(des, qn_f, r):
    rbase.gc()
    gc.collect()
    total_ci = svyciprop_yrbs(Formula(qn_f), des, multicore=True)
    # extract stats
    samps = pandas2ri.ri2py(sample_size(des))
    logger.info('fetching stats totals', r=r, d=samps)
    cts = rsvy.svyby(Formula(qn_f), Formula(qn_f), des, rsvy.unwtd_count, na_rm=True,
                     na_rm_by=True, na_rm_all=True, multicore=False)
    cts = pandas2ri.ri2py(cts)
    cols = ['eql', 'ct', 'se_ignore']
    cts.columns = cols
    ct = cts.ct[cts.eql==1].sum()
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
    logger.info('finished computation lvl1', res=res, total_ci=total_ci, ct=ct, ss=ss, s=samps)
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
    return u.fill_none(dfz) #.round(DECIMALS)


def subset(d, filter):
    return d._replace(des=subset_survey(d, filter))

def des_from_feather(fthr_file, denovo=False):
    rbase.gc()
    gc.collect()
    rdf = rfeather.read_feather(fthr_file)
    logger.info('creating survey design from data and annotations', cols=list(rbase.colnames(rdf)))
    strata = '~strata'
    if denovo:
        strata = '~year+strata'
    res = rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'), strata=Formula(strata), data=rdf, nest=True)
    rbase.gc()
    gc.collect()
    return res


def des_from_survey_db(tbl, db, host, port, denovo=False):
    strata = '~strata'
    if denovo:
        strata = '~yr+sitecode'
    return rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
                          strata=Formula(strata), nest=True,
                          data=tbl, dbname=db, host=host, port=port, dbtype='MonetDB.R')


