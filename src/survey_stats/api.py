import socket
import backtracepython as bt
import logging
from logging.handlers import SysLogHandler

from flask import Flask, redirect
from flask import request as req
from flask.json import jsonify
from werkzeug.routing import BaseConverter
from webargs import fields, ValidationError
from webargs.flaskparser import use_args, use_kwargs
from flasgger import Swagger

from survey_stats.survey import AnnotatedSurvey
from survey_stats.datasets import YRBSSDataset
from survey_stats.meta import SurveyMetadata
from survey_stats.error import InvalidUsage, EmptyFilterError, ComputationError
from survey_stats import settings
from survey_stats import state

app = Flask(__name__)
Swagger(app)
apst = {}


class ContextFilter(logging.Filter):
  hostname = socket.gethostname()

  def filter(self, record):
    record.hostname = ContextFilter.hostname
    return True


def boot_when_ready(server=None):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    f = ContextFilter()
    logger.addFilter(f)

    syslog = SysLogHandler(address=('logs5.papertrailapp.com', 16468))
    formatter = logging.Formatter('%(asctime)s %(hostname)s STATS: %(message)s', datefmt='%b %d %H:%M:%S')

    syslog.setFormatter(formatter)
    logger.addHandler(syslog)

    logger.info("This is a message")
    bt.initialize(endpoint=settings.BACKTRACE_URL,
                  token=settings.BACKTRACE_TKN)
    #fetch the state.metadata from Socrata
    apst['meta'] = SurveyMetadata.load_metadata('data/yrbss.yaml')
    #load survey datasets
    apst['yrbss'] = YRBSSDataset.load_dataset('data/yrbss.yaml')


class SurveyYearValidator(BaseConverter):
    """year(int) for which survey data is available."""

    def to_python(self, value):
        if not int(value) in apst['yrbss'].survey_years:
            raise ValueError('Selected year is not available!' + \
                             ' Choose from: %s' % str(apst['yrbss'].survey_years))
        return int(value)


    def to_url(self, value):
        return BaseConverter.to_url(str(value))

app.url_map.converters['survey_year'] = SurveyYearValidator
'''
def validated_facet(f):
    if not User.query.get(val):
        # Optionally pass a status_code
        raise ValidationError('User does not exist')

argmap = {
    'id': fields.Int(validate=must_exist_in_db)
}
'''
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


@app.errorhandler(404)
def fetch(err=None):
    return redirect('/apidocs/index.html')


@app.route("/questions")
@app.route("/questions/<survey_year:year>")
def fetch_questions(year=None):
    """
    Questions API
    Returns survey questions/columns along with
    associated metadata for the given year.
    ---
    tags:
      - questions
    parameters:
      - name: year
        in: path
        type: int
        required: false
    responses:
      200:
        description: list of available questions/columns in survey
        schema:
          id: QuestionList
          type: object
          additionalProperties: Question
    """
    def get_meta(k, v):
        key = k.lower()
        res = dict(apst['meta'].qnmeta_dict[key], **v, id=k) if key in \
            apst['meta'].qnmeta_dict else dict(v, id=k)
        return res
    national = True
    combined = False if year else True
    dset = apst['yrbss'].fetch_survey(combined, national, year)
    res = {k: get_meta(k,v) for k, v in dset.vars.items()}
    return jsonify(res)
"""
schema:
id: Question
type: object
properties:
id:
  type: string
  description: question id
is_integer:
  type: boolean
  description: column contains integer codings
question:
  type: string
  description: question text/prompt
responses:
  id: ResponseList
  type: array
  items:
    type: string

 """


@app.route('/stats/national')
@app.route('/stats/national/<survey_year:year>')
def fetch_national_stats(year=None):
    """
    National API
    Returns mean, CI and unweighted count for a national survey
    segment from either the combined or individual yearly datasets.
    ---
    tags:
      - stats/national
    parameters:
      - name: year
        in: path
        type: int
        required: false
      - name: q
        in: query
        type: string
        required: true
        description: question id
      - name: v
        in: query
        type: string
        required: false
        description: variables to break out/facet the population by
      - name: f
        in: query
        type: string
        required: false
        description: variable/value pairs to filter the population by
      - name: r
        in: query
        type: boolean
        default: true
        required: true
        description: responded true to the question prompt
    responses:
      200:
        description: list of available questions/columns in survey
        schema:
          id: StatsList
          type: array
          items:
            schema:
              id: Stats
              type: object
              properties:
                q:
                  type: string
                  description: question id
                question:
                  type: string
                  description: question text/prompt
                response:
                  type: boolean
                  description: responded true to the question prompt
                vars:
                  type: array
                  description: variables used to break out/facet the population
                  items:
                    type: string
                var_levels:
                  type: array
                  descriptions: levels/responses for each of the facet variables
                  items:
              id: Question
              type: object
              properties:
                id:
                  type: string
                  description: question id
                is_integer:
                  type: boolean
                  description: column contains integer codings
                question:
                  type: string
                  description: question text/prompt
                responses:
                  id: ResponseList
                  type: array
                  items:
                    type: string


    """
    return fetch_survey_stats(national=True, year=year)


@app.route('/stats/state')
def fetch_state_stats():
    """
    State API
    Returns mean, CI and unweighted count for a state survey
    segment from either the combined or individual yearly datasets.
    ---
    tags:
      - stats/state
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: question id
      - name: v
        in: query
        type: string
        required: false
        description: variables to break out/facet the population by
      - name: f
        in: query
        type: string
        required: false
        description: variable/value pairs to filter the population by
      - name: r
        in: query
        type: boolean
        default: true
        required: true
        description: responded true to the question prompt
    responses:
      200:
        description: list of available questions/columns in survey
        schema:
          id: StatsList
          type: array
          items:
            schema:
              id: Stats
              type: object
              properties:
                q:
                  type: string
                  description: question id
                question:
                  type: string
                  description: question text/prompt
                response:
                  type: boolean
                  description: responded true to the question prompt
                vars:
                  type: array
                  description: variables used to break out/facet the population
                  items:
                    type: string
                var_levels:
                  type: array
                  descriptions: levels/responses for each of the facet variables
                  items:
              id: Question
              type: object
              properties:
                id:
                  type: string
                  description: question id
                is_integer:
                  type: boolean
                  description: column contains integer codings
                question:
                  type: string
                  description: question text/prompt
                responses:
                  id: ResponseList
                  type: array
                  items:
                    type: string


    """
    return fetch_survey_stats(national=False, year=None)


def fetch_survey_stats(national, year):
    logging.info("requested uri: %s" % req.url)
    qn = req.args.get('q')
    vars = [] if not 'v' in req.args else req.args.get('v').split(',')
    resp = True if not 'r' in req.args else req.args.get('r')
    filt = {} if not 'f' in req.args else dict(map(lambda fv:
                                                   (fv.split(':')[0],
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
    if (len(in_both) > 0):
        raise InvalidUsage('Cannot have the same columns in filter and '+
                           'breakout variables! %s' % str(in_both))
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

if __name__ == '__main__':
    boot_when_ready()
    app.run(host='0.0.0.0', port=7777, debug=True)

