import io
import re
import zipfile
import pandas as pd
import asteval
from collections import OrderedDict
from cytoolz.itertoolz import mapcat
from cytoolz.curried import map, filter, curry
from cytoolz.functoolz import pipe, thread_last, identity
from dask import delayed
from survey_stats import log
from survey_stats.etl import survey_df as sdf
from survey_stats.etl import download as dl
from survey_stats.etl.sas import load_variable_labels

logger = log.getLogger(__name__)


def strip_line(l):
    # type: (str) -> str
    # strip whitespace and trailing period
    # and remove double quotes
    return l.strip().strip('.').replace('"','').replace("'","")


def parse_fwfcols_spss(spss_file, lgr=logger):
    # type: (str) -> OrderedDict
    """Extracts dat metadata from CDC YRBS SPSS files

    Extracts the col_specs from a CDC YRBS SPSS file. The col_specs
    are given as 3-tuples of (var, start, end) for each column in
    the fixed-width dat file.

    Args:
        spss_file: SPSS file path or file object

    Returns:
        colspecs: an `OrderedDict` colnames as keys, (st,en) as vals
    """

    def parse_field_span(span):
        """ parse start and end """
        try:
            (st, en) = span.split('-')
            ret = (int(st)-1,int(en))
        except Exception as e:
            raise ValueError("Improperly formed span in SPSS" +
                                     "file! %s -> %s" % (span, str(e)))
        return ret

    # if arg is filename, call self with open fh
    if not getattr(spss_file, 'read', False):
        x = dl.fetch_data_from_url(spss_file)
        t = x.read()
        t = t.decode('utf-8', errors='ignore') if type(t) is bytes else t
        spss_file = t.split('\n')
    col_specs = OrderedDict()
    widths_flag = False
    # extract fixed-width-field length rows
    for line in spss_file:
        if line.startswith('DATA LIST FILE'):
            widths_flag = True
            continue
        elif widths_flag and line.startswith('EXECUTE'):
            widths_flag = False
            break
        elif widths_flag:
            #parse a line with field widths
            #split on two consec spaces
            widths = strip_line(line).replace('(A)','').split()
            if not len(widths) % 2 == 0:
                raise ValueError("Invalid fixed-width field" +
                                    " definitions on line: %s" %
                                    strip_line(line))
            for i in range(0,len(widths),2):
                #iterate through pairs of var, span, and parse
                var = widths[i].lower()
                col_specs[var] = parse_field_span(widths[i+1])
            continue
        else:
            continue
    # - end for line in readline()...
    lgr.info('parsed col specs', cols=col_specs)
    return col_specs


def parse_surveyvars_spss(spss_file, lgr=logger):
    """Extracts dat metadata from CDC YRBS SPSS files

    Extracts the survey questions and responses from the
    CDC YRBS SPSS file.

    Args:
        spss_file: SPSS file path

    Returns:
        survey_vars: an OrderedDict with survey variables

        The resulting `survey_vars` is an OrderedDict with
        variable names as keys and dict values with fields of
        `question` containing the survey question, and `responses`
        containing a list of tuples of the form (resp_num, resp_label)
    """
    # if arg is filename, open it
    if not getattr(spss_file, 'read', False):
        x = dl.fetch_data_from_url(spss_file)
        t = x.read()
        t = t.decode('utf-8', errors='ignore') if type(t) is bytes else t
        spss_file = t.split('\n')

    survey_vars = OrderedDict()
    vars_flag = False
    vals_flag = False
    var = None
    vals = []
    # extract fixed-width-field length rows
    for line in spss_file:
        if line.startswith('VARIABLE LABELS'):
            vars_flag = True
            continue
        elif vars_flag and strip_line(line) == '':
            vars_flag = False
            continue
        elif vars_flag:
            #parse variable label
            # and add tuple (var, question/label)
            (var, q) =  strip_line(line).split(' ', 1)
            var = var.lower()
            survey_vars[var] = {
                'question': q,
                'responses': [],
                'is_integer': False
            }
        elif line.startswith('VALUE LABELS'):
            vals_flag = True
            vars_flag = False
            vals = []
            var = None
            continue
        elif vals_flag and line.startswith('/.'):
            #save the last var and val lbls
            #reset vals_flag
            survey_vars[var]['responses'] = vals[:]
            survey_vars[var]['is_integer'] = all(x[0].isdigit() for x in vals)
            var = None
            vals = []
            vals_flag = False
            continue
        elif vals_flag and line.strip() == '/':
            # save the last var and val lbls
            # reset
            survey_vars[var]['responses'] = vals[:]
            survey_vars[var]['is_integer'] = all(x[0].isdigit() for x in vals)
            var = None
            vals = []
            continue
        elif vals_flag and not var:
            # set the current var
            var = strip_line(line).lower()
            continue
        elif vals_flag and var:
            #add (num, label) to current list of val labels
            vals.append(tuple(
                strip_line(line).split(' ', 1) ))
            continue
        else:
            #default
            continue
    # - end for line in fh.readline()...
    lgr.info('parsed survey vars', v=survey_vars)
    return survey_vars


def load_survey_data(dat_f, svy_cols, lgr=logger):
    lgr.info('parsing raw survey data', f=dat_f, cols=svy_cols)
    df = pd.read_fwf(dat_f, 
                     colspecs=list(svy_cols.values()), 
                     names=list(svy_cols.keys()), 
                     na_values=['.',''])


def process_fwf_w_spss_loader(svy_cfg, facets, client=None, lgr=logger):
    g = svy_cfg
    prefix = g.s3_url_prefix
    lgr.bind(p=prefix)
    evalr = asteval.Interpreter()
    evalr.symtable['pd.util'] = pd.util
    fn = g.rename_cols
    map_fn = evalr(fn)
    df_munger = curry(sdf.munge_df)(facets=facets, qids=g.qids,
                                    na_syns=g.na_synonyms, col_fn=map_fn,
                                    fmts=g.patch_format, lgr=lgr)
    lbl_loader = curry(load_variable_labels)(repl=g.replace_labels)
    fwf_loader = curry(load_survey_data)(lgr=lgr)
    dfs = map(
        lambda r: pipe(prefix+r.fwf,
                       fwf_loader(svy_cols=parse_fwfcols_spss(prefix+r.spss, lgr=lgr)),
                       delayed(df_munger(r=r, lbls=lbl_loader(prefix+r.format, 
                                                              prefix+r.formas)))),
        [r for idx, r in g.meta.iterrows()])
    lgr.info('merging SAS dfs')
    dfs = delayed(pd.concat)(dfs, ignore_index=True)
    scols = delayed(
        lambda xf: list(xf.columns
                          .intersection(set(g.qids)
                                        .union(facets))))(dfs)
    lgr.info('re-filtering question and facet columns to cast to category dtype', cols=scols)
    dfz = (dfs
           .apply(lambda x: x.astype('category'))
           .reset_index(drop=True)
           .assign(year=dfs['year'].astype(int),
                   sitecode=dfs['sitecode'].astype('category'),
                   weight=dfs['weight'].astype(float),
                   strata=dfs['strata'].astype(int, errors='ignore'),
                   psu=dfs['psu'].astype(int, errors='ignore'))
           .reset_index(drop=True))
    dfz.visualize()
    lgr.info('merged SAS dfs')
    lgr.unbind('p')
    return dfz

