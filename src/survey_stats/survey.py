from parsers import cdc
from generative import GenerativeBase, _generative

CACHE_DIR = 'cache/'

svyciprop_yrbs = robjects.r('''
function(formula, design, method='xlogit', level = 0.95, df=degf(design), ...) {
    svyciprop(formula, design, method, level, df, na.rm=TRUE, ...)
}''')

svybyci_yrbs = robjects.r('''
function( formula, by, des, fn, ...) {
    svyby(formula, by, des, fn, keep_var=TRUE, method='xlogit',
          vartype=c('se','ci'), na.rm.by=TRUE, na.rm.all=TRUE, multicore=TRUE)
}''')


filter_var_levels = robjects.r('''
function(des, k, vals){
    des$variables[[k]] %in% vals
}
''')

#extend Series with fill_none method
# to take care of json/mysql conversion
def fill_none(self):
    return self.where(pd.notnull(self),None)
pd.Series.fill_none = fill_none

def guard_nan(val):
    return None if np.isnan(val) else val

def load_cdc_survey(spss_file, dat_file, resolve_cache_fn, survey_id):
    svy_cols = cdc.parse_fwfcols_spss(spss_file)
    svy_vars = cdc.parse_surveyvars_spss(spss_file)
    logging.info("Parsed SPSS metadata")

    rdf = None
    cache_file = '%s/%s.feather' % (CACHE_DIR, survey_id)

    try:
        rdf = rfther.read_feather(cache_file)
        logging.info('Loaded survey data from feather cache...')
    except:
        logging.warning("Could not find feather cache, loading raw data...")
        rdf = cdc.load_cdc_survey(dat_file, svy_cols, svy_vars)
        rfther.write_feather(rdf, 'data/yrbs.combined.feather')
        des = rsvy.svydesign(id=Formula("~psu"), weight=Formula("~weight"),
                             strata=Formula("~stratum"), data=data, nest=True)
    return (des, svy_vars)

def subset_survey(des, filt):
    #filt is a dict with vars as keys and list of acceptable values as levels
    #example from R:
    #  subset(dclus1, sch.wide=="Yes" & comp.imp=="Yes"
    if len(filt.keys()) > 0:
        filtered = rbase.Reduce( "&",
            [filter_var_levels(des, k, v) for k,v in filt.items()])
        return rsvy.subset_survey_design(des, filtered)
    else:
        #empty filter, return original design object
        return des

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

#idx = rdf.colnames.index('q3')

spss_file = 'data/YRBS_2015_SPSS_Syntax.sps'
dat_file = 'data/yrbs2015.dat'

spss_file = 'data/2015-sadc-spss-input-program.sps'
dat_file = 'data/sadc_2015_national.dat'

svy_cols = cdc.parse_fwfcols_spss(spss_file)
svy_vars = cdc.parse_surveyvars_spss(spss_file)
logging.info("Parsed SPSS metadata")

rdf = None

try:
    rdf = rfther.read_feather('cache/yrbs.combined.feather')
    logging.info('Loaded survey data from feather cache...')
except:
    logging.warning("Could not find feather cache, loading raw data...")
    rdf = cdc.load_survey(dat_file, svy_cols, svy_vars)
    rfther.write_feather(rdf, 'cache/yrbs.combined.feather')

yrbsdes = rsvy.svydesign(id=Formula('~psu'), weight=Formula('~weight'),
						 strata=Formula('~stratum'), data=rdf, nest=True)
'''
print("setup complete", )
sys.stdout.flush()
def test_fn(iter):
    print("%d - run 1" % iter)
    sys.stdout.flush()
    print(fetch_stats(yrbsdes, 'qn8', True, ['race7', 'sex']))
    print("%d - run 2" % iter)
    sys.stdout.flush()
#    fetch_stats(yrbsdes, 'qn8', True, ['q2', 'q3', 'raceeth'])
#    print("%d - run 3" % iter)
#    sys.stdout.flush()
#    fetch_stats(yrbsdes, 'qn8', True, ['q2', 'raceeth'])

for i in range(1):
    test_fn(i)
#sys.exit()
#print(timeit.timeit('test_fn()', number=10))
'''
d = {'grade': ['11th', '12th'],
      'race7': ['White', 'Asian'],
      'year': ['2011', '2013', '2015']}

res = fetch_stats( subset(yrbsdes, d), 'qn8', True, ['sex'] )
print(res, file=sys.stderr)
res = fetch_stats( yrbsdes, 'qn8', True, ['sex'] )
print(res, file=sys.stderr)
