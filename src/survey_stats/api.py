import backtracepython as bt
import pandas as pd
import logging
import hug
from survey import AnnotatedSurvey
from datasets import SurveyDataset

bt.initialize(
  endpoint="https://rootedinsights.sp.backtrace.io:6098",
  token="768367df71e2be15321e851494b6dcc7152bf8f48fe5cc85a2deac80b94a31e9"
)

logging.basicConfig(level=logging.DEBUG)

META_COLS = ['questioncode','shortquestiontext','description',
			 'greater_risk_question','lesser_risk_question','topic','subtopic']

META_URL = 'https://chronicdata.cdc.gov/resource/6ay3-nik2.json'
META_URL += '?$select={0},count(1)&$group={0}'.format(','.join(META_COLS))

def fetch_qn_meta():
	query = (META_URL)
	m = pd.read_json(query).fillna('')
	m['questioncode'] = m.questioncode.apply( lambda k: k.replace('H','qn') if k[0]=='H' else k.lower() )
	del m['count_1']
	m.set_index('questioncode', inplace=True, drop=False)
	return m.to_dict(orient="index")

class InvalidUsage(Exception):

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class EmptyFilterError(Exception):

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class ComputationError(Exception):

    def __init__(self, message, status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


#fetch the metadata from Socrata
meta = fetch_qn_meta()
#load survey datasets
yrbss = SurveyDataset.load_dataset('data/yrbss.yaml')
valid_years = {v['year']: int(v['year']) for v in yrbss.config.values()}
'''
@hug.type(extend=hug.types.number)
def valid_year(value):
    """Verify selected year is available."""
	valid = [v['year'] for v in yrbss.config.values()]:
    if not value in valid:
        raise ValueError('Data for selected year is not available!' + \
			'Choose from: %s' % ','.join(valid))
'''

@hug.local()
@hug.get(('/questions/{year}', '/questions'),
         examples=('/questions/2011','/questions'))
@hug.cli()
def fetch_questions(year:hug.types.mapping(valid_years)):
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
def fetch_national_stats(year:hug.types.mapping(valid_years)):
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

