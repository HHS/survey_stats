import pandas as pd
from cytoolz.functoolz import thread_first, thread_last
from cytoolz.itertoolz import concat
from cytoolz.curried import curry, map
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
from survey_stats.helpr import svyciprop_yrbs, svybyci_yrbs, subset_des_wexpr
from survey_stats.helpr import filter_survey_var
from survey_stats import pdutil as u
from survey_stats import log
from dask import delayed
import asyncio

rbase = importr('base')
rstats = importr('stats')
rpar = importr('parallel')
rsvy = importr('survey')

rfeather = importr('feather', on_conflict='warn')
rmonet = importr('MonetDB.R')

DECIMALS = {
    'mean': 4,
    'se': 4,
    'ci_l': 4,
    'ci_u': 4
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


def fetch_stats_by(des, qn_f, r, vs):
    lvl_f = '~%s' % '+'.join(vs)
    logger.info('gen stats for interaction level', vs=vs, r=r, lvl_f=lvl_f)
    lvl_f = Formula(lvl_f)
    cols = vs + ['mean', 'se', 'ci_l', 'ci_u']
    df = svybyci_yrbs(qn_f, lvl_f, des, svyciprop_yrbs) 
    df = pandas2ri.ri2py(df) if df is not None else pd.DataFrame(
        columns=['level','response']+cols)
    df.columns = cols
    logger.info('create svyby df', df=df, vars=vs)
    if df.shape[0] > 0:
        df['response'] = r
        df['level'] = len(vs)
    return u.fill_none(df.round(DECIMALS))

def fetch_stats_totals(des, qn_f, r):
    logger.info('fetching stats totals', r=r)
    total_ci = svyciprop_yrbs(qn_f, des, multicore=True, na_rm=True)
    # extract stats
    res = {'level': 0,
           'response': r,
           'mean': u.guard_nan(
               rbase.as_numeric(total_ci)[0]) if total_ci else None,
           'se': u.guard_nan(
               rsvy.SE(total_ci)[0]) if total_ci else None,
           'ci_l': u.guard_nan(
               rbase.attr(total_ci, 'ci')[0]) if total_ci else None,
           'ci_u': u.guard_nan(
               rbase.attr(total_ci, 'ci')[1]) if total_ci else None
           }
    # round as appropriate
    logger.info('finished computation lvl1', res=res, total_ci=total_ci)
    res = pd.DataFrame([res]).round(DECIMALS)
    return u.fill_none(res)


def mask_df(df, filt):
    # return a mask over the df for the given
    msk = df['yr'] > 1000
    for k, v in filt:
        if k == 'year':
            msk = msk & msk['yr'].isin(v) if len(v) > 1 else msk & msk['yr'] == v
        else:
            msk = msk & msk[k].isin(v) if len(v) > 1 else msk & msk[k] == v
    return msk

def fetch_sample_sizes(df, qn, vs, filt):
    msk = mask_df(rdf, filt)
    msk = msk & rdf[qn].where(pd.notnull)
    msk = msk & rdf[qn] == r
    rdf = df[msk][['yr',qn]+vs]
    

def fetch_stats(des, qn, r, vs=[], filt={}):
    # ex: ~qn8
    qn_f = Formula('~I(%s=="%s")' % (qn, r))
    logger.info('subsetting des with filter', filt=filt)
    des = subset_survey(des, filt)
    logger.info('done subsetting')
    dfs = [fetch_stats_totals(des, qn_f, r)]
    levels = [vs[:k+1] for k in range(len(vs))]
    sts = map(lambda lvl: fetch_stats_by(des, qn_f, r, lvl), levels)
    dfz = pd.concat(res + sts)
    # get stats_by_fnats for each level of interactions in vars
    # using svyby to compute across combinations of loadings
    logger.info('finished computations, appending dfs', dfs=dfs)
    return u.fill_none(dfz) #.round(DECIMALS)


def sample_size(d):
    return rbase.dim(d[d.names.index('variables')])[0]


def subset(d, filter):
    return d._replace(des=subset_survey(d, filter))


def des_from_feather(fthr_file, denovo=False):
    rdf = rfeather.read_feather(fthr_file)
    logger.info('creating survey design from data and annotations', cols=list(rbase.colnames(rdf)))
    strata = '~strata'
    if denovo:
        strata = '~year+strata'
    return rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
                          strata=Formula(strata), data=rdf, nest=True)


def des_from_survey_db(tbl, db, host, port, denovo=False):
    strata = '~strata'
    if denovo:
        strata = '~yr+sitecode'
    return rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
                          strata=Formula(strata), nest=True,
                          data=tbl, dbname=db, host=host, port=port, dbtype='MonetDB.R')


