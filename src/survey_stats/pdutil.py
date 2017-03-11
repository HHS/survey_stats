import pandas as pd
import numpy as np
import logging
from toolz.functoolz import thread_last, thread_first, flip, do, compose
from toolz.itertoolz import concat, concatv, mapcat
from toolz.curried import map, filter, reduce
from toolz import curry

#extend Series with fill_none method
# to take care of json/mysql conversion
def fill_none(self):
    return self.where(pd.notnull(self),None)

def guard_nan(val):
    return None if np.isnan(val) else val


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
            lvls= ','.join(map(lambda x:'"%s"' %x, v)) if
                type(v) == list else
                '"%s"' % v
        ) for k,v in filt.items()
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
    logging.warn(z)
    return ' & '.join(['%s == "%s"' % (k,v) for k,v in z.items()])

def tee_logfn(x):
    """
    tee operator that logs and then returns x
    for logging intermediate results in a
    pipeline
    """
    return do(logging.info, x)
