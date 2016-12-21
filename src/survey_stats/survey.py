from parsers import cdc

def default_resolve_cache_fn(survey_id):
    raise NotImplementedError('Default cache resolution is not implemented!')

class Survey(object):
    def __init__(self, data, survey_vars):
        self.df = data
        self.vars = survey_vars
        self.des = rsvy.svydesign(id=Formula("~psu"), weight=Formula("~weight"),
                                strata=Formula("~stratum"), data=rdf, nest=True)
    @classmethod
    def load_cdc_survey(spss_file, dat_file, resolve_cache_fn, survey_id):
        svy_cols = cdc.parse_fwfcols_spss(spss_file)
        svy_vars = cdc.parse_surveyvars_spss(spss_file)
        logging.info("Parsed SPSS metadata")

        rdf = None

        try:
            rdf = rfther.read_feather('data/yrbs.combined.feather')
            logging.info('Loaded survey data from feather cache...')
        except:
            logging.warning("Could not find feather cache, loading raw data...")
            rdf = cdc.load_cdc_survey(dat_file, svy_cols, svy_vars)
            rfther.write_feather(rdf, 'data/yrbs.combined.feather')



spss_file = 'data/YRBS_2015_SPSS_Syntax.sps'
dat_file = 'data/yrbs2015.dat'

spss_file = 'data/2015-sadc-spss-input-program.sps'
dat_file = 'data/sadc_2015_national.dat'

#svyciprop_yrbs = rfunc.Curry(rsvy.svyciprop, method='xlogit', level=0.95,
#                             na_rm=True)
#svybyci_yrbs = rfunc.Curry(rsvy.svyby, keep_var=True, method='xlogit',
#                           vartype=robjects.vectors.StrVector(['se','ci']),
#                           na_rm_by=True, na_rm_all=True, multicore=True)
svyciprop_yrbs = robjects.r('''
function(formula, design, method='xlogit', level = 0.95, df=degf(design), ...) {
    svyciprop(formula, design, method, level, df, na.rm=TRUE, ...)
}''')

svybyci_yrbs = robjects.r('''
function( formula, by, des, fn, ...) {
    svyby(formula, by, des, fn, keep_var=TRUE, method='xlogit',
          vartype=c('se','ci'), na.rm.by=TRUE, na.rm.all=TRUE, multicore=TRUE)
}''')


'''sample calls
robjects.globalenv['yrbsdes'] = yrbsdes
robjects.globalenv['rdf'] = rdf
rbase.save('yrbsdes', 'rdf', file='save.RData')

ci = svyciprop_yrbs(Formula('~!qn8'), yrbsdes, na_rm=True,
method='xlogit')

byci = rsvy.svyby(Formula('~!qn8'), Formula('~q2 + raceeth'),
yrbsdes, rsvy.svyciprop, method='xlogit',
na_rm=True, vartype=StrVector(['se','ci']))

byct = rsvy.svyby(Formula('~!qn8'), Formula('~q2 + raceeth'),
yrbsdes, rsvy.unwtd_count, na_rm=True)

'''
#extend Series with fill_none method
# to take care of json/mysql conversion
def fill_none(self):
    return self.where(pd.notnull(self),None)
pd.Series.fill_none = fill_none

def fetch_stats(des, qn, response=True, vars=[]):
    DECIMALS = {
        'mean': 4, 'se': 4, 'ci_l': 4, 'ci_u': 4, 'count':0
    }
    def fetch_stats_by(vars, qn_f, des):
        lvl_f = Formula('~%s' % ' + '.join(vars))
        #svyciprop_local =
        ci = svybyci_yrbs(qn_f, lvl_f, des, svyciprop_yrbs)
        ct = rsvy.svyby(qn_f, lvl_f, des, rsvy.unwtd_count, na_rm=True,
                        na_rm_by=True, na_rm_all=True, multicore=True)
        merged = pandas2ri.ri2py(rbase.merge(ci, ct))
        del merged['se']
        ci_struct = ci.__sexp__
        ct_struct = ct.__sexp__
        del(ci)
        del(ct)
        del(ci_struct)
        del(ct_struct)
        merged.columns = vars + ['mean', 'se', 'ci_l', 'ci_u', 'count']
        merged['level'] = len(vars)
        merged['q'] = qn
        merged['q_resp'] = response
        merged = merged.round(DECIMALS)
        return merged.apply(lambda r: r.fill_none().to_dict(), axis=1)
    # create formula for selected question and risk profile
    # ex: ~qn8, ~!qn8
    qn_f = Formula('~%s%s' % ('' if response else '!', qn))
    total_ci = svyciprop_yrbs(qn_f, des, multicore=True)
    total_ct = rsvy.unwtd_count(qn_f, des, na_rm=True, multicore=True)
    #extract stats
    res = { 'level': 0,
           'mean': rbase.as_numeric(total_ci)[0],
           'se': rsvy.SE(total_ci)[0],
           'ci_l': rbase.attr(total_ci,'ci')[0],
           'ci_u': rbase.attr(total_ci,'ci')[1],
           'count': rbase.as_numeric(total_ct)[0]}
    ci_struct = total_ci.__sexp__
    ct_struct = total_ct.__sexp__
    del(total_ci)
    del(total_ct)
    del(ci_struct)
    del(ct_struct)
    #round as appropriate
    res = {k: round(v, DECIMALS[k]) if k in DECIMALS else v for k,v in
           res.items()}
    #setup the result list
    res = [res]
    vstack = vars[:]
    while len(vstack) > 0:
        #get stats for each level of interactions in vars
        #using svyby to compute across combinations of loadings
        res.extend(fetch_stats_by(vstack, qn_f, des))
        vstack.pop()
        return res



