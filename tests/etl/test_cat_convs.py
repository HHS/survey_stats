from cytoolz.curried import curry
from cytoolz.itertoolz import unique
import numpy as np
import pandas as pd
import pandas.util.testing as pt
from hypothesis import given, assume
import hypothesis.strategies as hs
import hypothesis.extra.numpy as hnp
from faker import Faker

from survey_stats.etl.survey_df import convert_cat_codes, convert_cat_force, eager_convert

fake = Faker()

FORMATS = {
    'VAR1' : {
        1: '9th Grade',
        2: '10th Grade',
        3: '11th Grade',
        4: '12th Grade',
        5: 'Ungraded or other grade' },
    'VAR2':{
        1: 'Yes',
        2: 'No',
        7: 'DK/NS',
        9: 'DK/NS'
    }}


fmtgen = hs.dictionaries(keys=hs.sets(hs.integers(min_value=1, max_value=100)),
                         values=hs.lists(hs.sampled_from(fake.words(nb=100))),
                         min_size=2, average_size=4, max_size=60)


def gen_codes_for_fmt(fmt, include_nas=False, valid_only=True):
    elems = None if not valid_only \
                 else hs.sampled_from(
                     sorted(fmt.keys()) + [np.nan] if include_nas \
                                                   else sorted(fmt.keys()))
    dtypes = hnp.floating_dtypes(endianness='=') \
                if include_nas or valid_only \
                else hs.one_of(hnp.floating_dtypes(endianness='='),
                               hnp.integer_dtypes(endianness='='))
    return hnp.arrays(dtype=dtypes,
                      shape=hnp.array_shapes(max_dims=1, max_side=1000),
                      elements=elems)



def validate_cats_for_fmt(x, fmtid, convfn):
    fmt = FORMATS[fmtid]
    fmt_lvls = list(unique([fmt[k] for k in sorted(fmt.keys())]))
    xs = pd.Series(x, name=fmtid)
    xc = convfn(xs, fmt)
    assert type(xc) == type(xs)
    assert xc.dtype.name == 'category'
    assert list(xc.cat.categories) == fmt_lvls
    vc = xc.value_counts().to_dict()
    assert set(vc.keys()) == set(fmt.values())
    return xc


@given(x=gen_codes_for_fmt(FORMATS['VAR1'], include_nas=False))
def test_convert_valid_codes_no_dup_labels_no_nas(x):
    s1 = validate_cats_for_fmt(x, 'VAR1', convert_cat_codes)
    s2 = validate_cats_for_fmt(x, 'VAR1', convert_cat_force)
    s3 = validate_cats_for_fmt(x, 'VAR1', eager_convert)
    pt.assert_series_equal(s1,s2)
    pt.assert_series_equal(s1,s3)
    pt.assert_series_equal(s2,s3)


@given(x=gen_codes_for_fmt(FORMATS['VAR1'], include_nas=True))
def test_convert_valid_codes_no_dup_labels_w_nas(x):
    s1 = validate_cats_for_fmt(x, 'VAR1', convert_cat_codes)
    s2 = validate_cats_for_fmt(x, 'VAR1', convert_cat_force)
    s3 = validate_cats_for_fmt(x, 'VAR1', eager_convert)
    pt.assert_series_equal(s1,s2)
    pt.assert_series_equal(s1,s3)
    pt.assert_series_equal(s2,s3)


@given(x=gen_codes_for_fmt(FORMATS['VAR2'], include_nas=False))
def test_convert_valid_codes_w_dup_labels_no_nas(x):
    s2 = validate_cats_for_fmt(x, 'VAR2', convert_cat_force)
    s3 = validate_cats_for_fmt(x, 'VAR2', eager_convert)
    pt.assert_series_equal(s2,s3)


@given(x=gen_codes_for_fmt(FORMATS['VAR2'], include_nas=True))
def test_convert_valid_codes_w_dup_labels_w_nas(x):
    s2 = validate_cats_for_fmt(x, 'VAR2', convert_cat_force)
    s3 = validate_cats_for_fmt(x, 'VAR2', eager_convert)
    pt.assert_series_equal(s2,s3)


@given(x=gen_codes_for_fmt(FORMATS['VAR1'], valid_only=False))
def test_convert_invalid_codes_no_dup_labels(x):
    fmt = FORMATS['VAR1']
    fmt_lvls = set(fmt.keys())
    xs = pd.Series(x, name='VAR1')
    # ensure that we have more values than just the keys
    assume(len(set(xs.dropna()).difference(fmt_lvls)) > 0)
    xc = eager_convert(xs, fmt)
    pt.assert_series_equal(xs, xc)


@given(x=gen_codes_for_fmt(FORMATS['VAR2'], valid_only=False))
def test_convert_invalid_codes_w_dup_labels(x):
    fmt = FORMATS['VAR2']
    fmt_lvls = set(fmt.keys())
    xs = pd.Series(x, name='VAR2')
    # ensure that we have more values than just the keys
    assume(len(set(xs.dropna()).difference(fmt_lvls)) > 0)
    xc = eager_convert(xs, fmt)
    pt.assert_series_equal(xs, xc)


