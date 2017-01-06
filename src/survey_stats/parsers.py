import pandas as pd
import logging
from collections import OrderedDict

import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import pandas.rpy.common as com

import helpr

pandas2ri.activate()

rbase = importr('base')


def strip_line(l):
    # type: (str) -> str
    # strip whitespace and trailing period
    # and remove double quotes
    return l.strip().strip('.').replace('"','').replace("'","")


class ParseSPSSException(Exception):
    pass

class ParseCDCSurveyException(Exception):
    pass


def parse_fwfcols_spss(spss_file):
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
            raise ParseSPSSException("Improperly formed span in SPSS" +
                                     "file! %s -> %s" % (span, str(e)))
        return ret

    # if arg is filename, call self with open fh
    if not getattr(spss_file, 'read', False):
        with open(spss_file, 'r') as fh:
            return parse_fwfcols_spss(fh)

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
                raise ParseSPSSException("Invalid fixed-width field" +
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
    return col_specs


def parse_surveyvars_spss(spss_file):
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
    # if arg is filename, call self with open fh
    if not getattr(spss_file, 'read', False):
        with open(spss_file, 'r') as fh:
            return parse_surveyvars_spss(fh)

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
    return survey_vars


class ParseCDCSurveyException(Exception):
    pass

def load_survey(dat_files, svy_cols, svy_vars):
    logging.info('parsing raw survey data: %s' % ','.join(dat_files))
    df = pd.concat(map(lambda dat_f: pd.read_fwf(dat_f,
                                                 colspecs=list(svy_cols.values()),
                                                 names=list(svy_cols.keys()),
                                                 na_values=['.','']),
                       dat_files), ignore_index=True, copy=False)
    logging.info('converting survey data to R object')
    rdf = com.convert_to_r_dataframe(df)
    logging.info('coercing variables to annotated types')
    for q, v in svy_vars.items():
        if v['is_integer']:
            (codes, cats) = zip(*v['responses'])
            idx = rdf.colnames.index(q)
            fac = rdf[idx]
            try:
                fac = rbase.as_integer(fac)
                fac = rbase.factor(fac, levels=list(codes), labels=list(cats))
                rdf[idx] = fac
            except:
                logging.error(rbase.summary(rdf[idx]))
                logging.error(helpr.factor_summary(rdf[idx]))
                logging.error(rbase.summary(fac))
                bt.send_last_exception()
                raise ParseCDCSurveyException('parsing problems: %s -> %s'
                                              % (q, v))
        elif q.startswith('qn'):
            idx = rdf.colnames.index(q)
            fac = rbase.as_integer(rdf[idx])
            coerced = rbase.is_na(fac)
            n_coerced = rbase.sum(coerced)[0]
            if n_coerced > 0:
                coerced = helpr.factor_summary(rdf[idx].rx(coerced))
                logging.warning('Coerced non-numeric values for variable:' +
                                ' %s\n%s' % (q, coerced))
            if rbase.min(fac, na_rm=True)[0] < 1 or \
               rbase.max(fac, na_rm=True)[0] > 2:
                raise ParseCDCSurveyException('Found invalid levels for' +
                                              ' boolean var: %s -> %s' %
                                              (q, helpr.factor_summary(fac)))
            rdf[idx] = helpr.tobool(fac)
    return rdf

'''
def load_survey_py(dat_file, svy_cols, svy_vars):
    df = pd.read_fwf(dat_file, colspecs=list(svy_cols.values()),
                     names=list(svy_cols.keys()), na_values=['.',''])
    logging.info('Parsed raw survey data')
    for q, v in svy_vars.items():
        if v['is_integer']:
            (codes, cats) = zip(*v['responses'])
            try:
                df[q] = pd.Categorical.from_codes(df[q].fillna(-1),
                                                  categories=list(cats),
                                                  ordered=True)
            except:
                logging.error(df[q].describe())
                raise ParseCDCSurveyException('parsing problems: %s -> %s'
                                              % (q, v))
        elif q.startswith(BOOLEAN_RESPONSE_PREFIX):
            idx = rdf.colnames.index(q)
            fac = rbase.as_integer(rdf[idx])
            coerced = rbase.is_na(fac)
            n_coerced = rbase.sum(coerced)[0]
            if n_coerced > 0:
                coerced = helpr.factor_summary(rdf[idx].rx(coerced))
                logging.warning('Coerced non-numeric values for variable:' +
                                ' %s\n%s' % (q, coerced))
            if rbase.min(fac, na_rm=True)[0] < 1 or \
               rbase.max(fac, na_rm=True)[0] > 2:
                raise ParseCDCSurveyException('Found invalid levels for' +
                                              ' boolean var: %s -> %s' %
                                              (q, helpr.factor_summary(fac)))
            rdf[idx] = tobool(fac)
    rdf = com.convert_to_r_dataframe(df)
    logging.info('Converted survey data to R object')
    return rdf
'''
