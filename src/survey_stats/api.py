import backtracepython as bt
import pandas as pd
import logging
import hug
from survey import AnnotatedSurvey
from datasets import YRBSSDataset
from meta import fetch_yrbss_meta
from error import *

bt.initialize(
  endpoint="https://rootedinsights.sp.backtrace.io:6098",
  token="768367df71e2be15321e851494b6dcc7152bf8f48fe5cc85a2deac80b94a31e9"
)

logging.basicConfig(level=logging.DEBUG)


#fetch the metadata from Socrata
meta = fetch_qn_meta()
#load survey datasets
yrbss = YRBSSDataset.load_dataset('data/yrbss.yaml')
#enumerate the

@hug.type(extend=hug.types.number)
def valid_year(value):
    """Verify selected year is available."""
    if not value in yrbss.survey_years:
        raise ValueError('Data for selected year is not available!' + \
			'Choose one of: %s' % ','.join(valid))


"""
    qn = req.args.get('q')
    vars = [] if not 'v' in req.args else req.args.get('v').split(',')
    resp = True if not 'r' in req.args else int(req.args.get('r')) > 0
    filt = {} if not 'f' in req.args else dict(map(lambda fv:
                                                   (fv.split(':')[0],
                                                    fv.split(':')[1].split(',')),
                                                    req.args.get('f').split(';')))
"""

@hug.local()
@hug.get(('/questions/{year}', '/questions'),
         examples=('/questions/2011','/questions'))
@hug.cli()
def fetch_questions(year:valid_year):
    def get_meta(k, v):
        key = k.lower()
        res = dict(meta[key], **v) if key in meta else v
        return res
    combined = True
    national = True
    if year and year in range(1993, 2017, 2):
        combined = False
    dset = yrbss.fetch_survey(combined, national, year)
    res = {k: get_meta(k,v) for k, v in dset.vars.items()}
    return jsonify(res)

@hug.local()
@hug.get(('/stats/year/{year}', '/stats/year'),
         examples=('/stats/year/2011','/stats/year'))
@hug.cli()
def fetch_national_stats(year:valid_year):
    return fetch_survey_stats(national=True, year=year)

@hug.local()
@hug.get('/stats/state', examples='')
@hug.cli()
def fetch_state_stats():
    return fetch_survey_stats(national=False, year=None)


def fetch_survey_stats(national, year):
    logging.info("requested uri: %s" % req.url)
    qn = req.args.get('q')
    vars = [] if not 'v' in req.args else req.args.get('v').split(',')
    resp = True if not 'r' in req.args else int(req.args.get('r')) > 0
    filt = {} if not 'f' in req.args else dict(map(lambda fv:
                                                   (fv.split(':')[0],
                                                    fv.split(':')[1].split(',')),
                                                    req.args.get('f').split(';')))

    logging.info(filt)
    combined = True
    if year and year in range(1993, 2017, 2):
        combined = False

    # update vars and filt column names according to pop_vars
    (k, cfg) = yrbss.fetch_config(combined, national, year)
    logging.info((k, cfg))
    replace_f = lambda x: cfg['pop_vars'][x] if x in cfg['pop_vars'] else x
    logging.info(vars)
    logging.info(filt)
    m_vars = list(map(replace_f, vars))
    m_filt = {replace_f(k): v for k,v in filt.items()}
    svy = yrbss.surveys[k]
    svy = svy.subset(m_filt)

    if not svy.sample_size > 1:
        raise EmptyFilterError('EmptyFilterError: %s' % (str(m_filt)))
    ivd = {v: k for k, v in cfg['pop_vars'].items()}

    #setup functions to reverse map keys for stats
    inverse_f = lambda x: ivd[x] if x in ivd else x
    replkeys_f = lambda d: {inverse_f(k): v for k,v in d.items()}

    try:
        question = svy.vars[qn]['question']
        var_levels = {inverse_f(v): svy.vars[v] for v in m_vars}
    except KeyError as  err:
        raise InvalidUsage('KeyError: %s' % str(err))
    try:
        stats = svy.fetch_stats(qn, resp, m_vars)
        stats = list(map(replkeys_f, stats))
        return jsonify({
            'q': qn,
            'question': question,
            'response': resp,
            'vars': vars,
            'var_levels': var_levels,
            'results': stats
        })
    except KeyError as  err:
        raise InvalidUsage('KeyError: %s' % str(err))
    except Exception as err:
        raise ComputationError('Error computing stats! %s' % str(err))


if __name__=='__main__':
    app.run(host="0.0.0.0", port=7777, debug=True)

