import sys
sys.path.append('src/survey_stats')

import parsers.cdc_yrbs as cdc
import survey

logging.basicConfig(level=logging.DEBUG)



#idx = rdf.colnames.index('q3')

'''
print("setup complete")
sys.stdout.flush()
def test_fn(iter):
    print("%d - run 1" % iter)
    sys.stdout.flush()
    fetch_stats(yrbsdes, 'qn8', True, ['q2', 'q3'])
    print("%d - run 2" % iter)
    sys.stdout.flush()
    fetch_stats(yrbsdes, 'qn8', True, ['q2', 'q3', 'raceeth'])
    print("%d - run 3" % iter)
    sys.stdout.flush()
    fetch_stats(yrbsdes, 'qn8', True, ['q2', 'raceeth'])

for i in range(10):
    test_fn(i)
sys.exit()
#print(timeit.timeit('test_fn()', number=10))
'''

META_COLS = ['year','questioncode','shortquestiontext','description',
			 'greater_risk_question','lesser_risk_question','topic','subtopic']

META_URL = 'https://chronicdata.cdc.gov/resource/6ay3-nik2.json'
META_URL += '?$select={0},count(1)&$group={0}'.format(','.join(META_COLS))

def fetch_qn_meta():
	query = (META_URL)
	m = pd.read_json(query).fillna('')
	m['questioncode'] = m.questioncode.apply( lambda k: k.replace('H','qn') if k[0]=='H' else k.lower() )
	del m['count_1']
	m.set_index(['year','questioncode'], inplace=True, drop=False)
	return m.to_dict(orient="index")

#app = Sanic(__name__)
from flask import Flask
from flask import request as req
from flask.json import jsonify

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


rbase.gc()
app = Flask(__name__)
meta = fetch_qn_meta()

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(ComputationError)
def handle_computation_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/questions")
def fetch_questions(year=2015):
	def get_meta(k, v, yr=year):
		key = (2015,k.lower())
		res = dict(meta[key], **v) if key in meta else v
		return res
	res = {k: get_meta(k,v) for k, v in svy_vars.items()}
	return jsonify(res)


@app.route("/national")
def fetch_national():
    rbase.gc()
    qn = req.args.get('q')
    vars = [] if not 'v' in req.args else req.args.get('v').split(',')
    resp = True if not 'r' in req.args else int(req.args.get('r')) > 0
    try:
        return jsonify({
            "q": qn,
            "question": svy_vars[qn]['question'],
            "response": resp,
            "vars": vars,
            "var_levels": {v: svy_vars[v] for v in vars},
            "results": fetch_stats(yrbsdes, qn, resp, vars)
        })
    except KeyError as  err:
        raise InvalidUsage('KeyError: %s' % str(err))
    except Exception as err:
        raise ComputationError('Error computing stats! %s' % str(err))


if __name__=='__main__':
    app.run(host="0.0.0.0", port=7777, debug=True)

