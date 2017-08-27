from cytoolz.dicttoolz import valmap
from survey_stats.etl.sas import block2dict, parse_variable_labels
from .format_fixtures import FORMATS, FMTDICT


def run_test_for_fmt_ver(version, repl):
    r = FMTDICT[version]
    f = FORMATS[version]
    d = parse_variable_labels(f, repl=repl, lbls_to_lower=False)
    assert set(d.keys()) == set(r.keys())
    for k in r.keys():
        assert d[k] == r[k]
    d = parse_variable_labels(f, repl=repl, lbls_to_lower=True)
    assert set(d.keys()) == set(r.keys())
    for k in r.keys():
        assert d[k] == valmap(str.lower, r[k])


def test_parse_no_repl_no_singlequot_no_quotedcodes_no_multiassign():
    run_test_for_fmt_ver('V2', repl={})

def test_parse_no_repl_w_singlequot_no_quotedcodes_w_multiassign():
    run_test_for_fmt_ver('V3', repl={})

def test_parse_no_repl_no_singlequot_w_quotedcodes_no_multiassign():
    run_test_for_fmt_ver('V1', repl={})
