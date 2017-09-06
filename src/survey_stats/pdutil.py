import pandas as pd
import numpy as np
from survey_stats import log
from cytoolz.functoolz import do

logger = log.getLogger()


def undash(col):
    return 'x' + col.lower() if col[0] == '_' else col.lower()

def div100(col):
    return pd.to_numeric(col, errors='coerce') / 100.0

# extend Series with fill_none method
# to take care of json/mysql conversion
def fill_none(df):
    return df.where(pd.notnull(df), None)


def guard_nan(val):
    return None if np.isnan(val) else val


def factor_summary(df):
    return df.dtypes.value_counts(dropna=False)


def duplicated_varnames(df):
    """Return a dict of all variable names that
    are duplicated in a given dataframe."""
    repeat_dict = {}
    var_list = list(df)  # list of varnames as strings
    for varname in var_list:
        # make a list of all instances of that varname
        test_list = [v for v in var_list if v == varname]
        # if more than one instance, report duplications in repeat_dict
        if len(test_list) > 1:
            repeat_dict[varname] = len(test_list)
    return repeat_dict


def fmla_for_filt(filt):
    """
    transform a set of column filters
    from a dictionary like
        { 'varX':['lv11','lvl2'],...}
    into an R selector expression like
        'varX %in% c("lvl1","lvl2")' & ...
    """
    return ' & '.join([
        '{var} %in% c({lvls})'.format(
            var=k,
            lvls=','.join(map(lambda x:'"%s"' % x, v)) if
            type(v) == list else '"%s"' % v
        ) for k, v in filt.items()
    ])


def fmla_for_slice(z):
    """
    convert from column selector row (in dataframe) like
        ('varX','lvl1'),('varY','lvl3'),('varZ','lvl0')...
    to a set of R selector expression like
        'varX == "lvl1"'
        'varX == "lvl1" & varY == "lvl3"'
        'varX == "lvl1" & varY == "lvl3" & varZ == "lvl0"'
    """
    logger.info('creating formula for slice', slice=z)
    return ' & '.join(['%s == "%s"' % (k, v) for k, v in z.items()])


def tee_logfn(lgr, x):
    """
    tee operator that logs and then returns x
    for logging intermediate results in a
    pipeline
    """
    return do(lgr.info, x)
