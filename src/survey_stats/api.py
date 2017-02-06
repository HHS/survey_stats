import time
from collections import OrderedDict
from flask import Flask, redirect, g, render_template
from flask import request as req
from flask.json import jsonify
from survey_stats.survey import AnnotatedSurvey
from survey_stats.datasets import YRBSSDataset
from survey_stats.meta import SurveyMetadata
from survey_stats.error import InvalidUsage, EmptyFilterError, ComputationError
from survey_stats import settings
from survey_stats import state
from survey_stats.validate import (SurveyYearValidator, validated_facet,
                                   handle_invalid_usage, fetch, before_request)

app = None

def boot_when_ready(server=None):
    app = Flask(__name__)
    app.url_map.converters['survey_year'] = validate.SurveyYearValidator


@app.route("/questions")
@app.route("/questions/<survey_year:year>")
def fetch_questions(year=None):


@app.route('/stats/national')
@app.route('/stats/national/<survey_year:year>')
def fetch_national_stats(year=None):
    """
    National API
    Returns mean, CI and unweighted count for a national survey
    segment from either the combined or individual yearly datasets.
    """
    return fetch_survey_stats(national=True, year=year)


@app.route('/stats/state')
def fetch_state_stats():
    """
    State API
    Returns mean, CI and unweighted count for a state survey
    segment from either the combined or individual yearly datasets.
    """
    return fetch_survey_stats(national=False, year=None)


def fetch_survey_stats(national, year):
    logging.info("requested uri: %s" % req.url)
    qn = req.args.get('q')
    vars = [] if not 'v' in req.args else req.args.get('v').split(',')
    resp = True if not 'r' in req.args else not 0 ** int(req.args.get('r'),2)
    filt = {} if not 'f' in req.args else dict(
        map(lambda fv: (fv.split(':')[0],
                        fv.split(':')[1].split(',')),
            req.args.get('f').split(';')))
    logging.info(filt)
    combined = True
    if year:
        combined = False
    # update vars and filt column names according to pop_vars
    (k, cfg) = apst['yrbss'].fetch_config(combined, national, year)
    logging.info((k, cfg))
    replace_f = lambda x: cfg['pop_vars'][x] if x in cfg['pop_vars'] else x
    logging.info(vars)
    logging.info(filt)
    m_vars = list(map(replace_f, vars))
    m_filt = {replace_f(k): v for k,v in filt.items()}
    in_both = set(m_vars).intersection(m_filt)
    svy = apst['yrbss'].surveys[k]
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
    except KeyError as err:
        raise InvalidUsage('KeyError: %s' % str(err), payload={
            'traceback': traceback.format_exc().splitlines(),
            'request': req.args.to_dict(),
            'state': {
                'q': qn,
                'svy_vars': svy.vars,
                'm_vars': m_vars
            }})
    try:
        logging.info("Ready to fetch!")
        stats = svy.fetch_stats(qn, resp, m_vars, m_filt)
        g_time = g.request_time()
        logging.info('elapsed_time', g_time)
        stats = list(map(replkeys_f, stats))
        return jsonify({
            'q': qn,
            'filter': filt,
            'question': question,
            'response': resp,
            'vars': vars,
            'var_levels': var_levels,
            'results': stats,
            '_elapsed_time': g_time
        })
    except KeyError as  err:
        raise InvalidUsage('KeyError: %s' % str(err), payload={
            'traceback': traceback.format_exc().splitlines(),
            'request': req.args.to_dict(),
            'state': {
                'q': qn,
                'svy_vars': svy.vars,
                'm_vars': m_vars,
                'filter': filt,
                'response': resp,
                'var_levels': var_levels
            }})


if __name__ == '__main__':
    boot_when_ready()
    app.run(host='0.0.0.0', port=7777, debug=True)

