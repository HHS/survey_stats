import backtracepython as bt
import logging
from flask import Flask
from flask import request as req
from flask.json import jsonify
from survey_stats.survey import AnnotatedSurvey
from survey_stats.datasets import YRBSSDataset
from survey_stats.meta import fetch_yrbss_meta
from survey_stats.error import InvalidUsage, EmptyFilterError, ComputationError
from survey_stats import settings

meta = None
yrbss = None
app = Flask(__name__)


def boot_when_ready(server=None):
    global meta
    global yrbss
    logging.basicConfig(level=logging.DEBUG)
    bt.initialize(endpoint=settings.BACKTRACE_URL,
                  token=settings.BACKTRACE_TKN)
    #fetch the metadata from Socrata
    meta = fetch_yrbss_meta()
    #load survey datasets
    yrbss = YRBSSDataset.load_dataset('data/yrbss.yaml')


def valid_year(value):
    """year(int) for which survey data is available."""
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


@app.errorhandler(InvalidUsage)
@app.errorhandler(EmptyFilterError)
@app.errorhandler(ComputationError)
def handle_invalid_usage(error):
    bt.send_last_exception()
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/questions")
@app.route("/questions/<int:year>")
def fetch_questions(year=None):
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


@app.route('/stats/national')
@app.route('/stats/national/<int:year>')
def fetch_national_stats(year=None):
    return fetch_survey_stats(national=True, year=year)


@app.route('/stats/state')
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
    #except Exception as err:
    #    raise ComputationError('Error computing stats! %s' % str(err))

if __name__ == '__main__':
    boot_when_ready()
    app.run(host='0.0.0.0', port=7777, debug=True)

