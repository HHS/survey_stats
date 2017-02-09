from flask import Flask, redirect, g, render_template
from flask import request as req
from flask.json import jsonify
import logging
from survey_stats import log
from survey_stats import settings
from survey_stats import state as st

app = Flask(__name__)

logging.info(st.dset.keys())
logging.info(st.dset['yrbss'].surveys.keys())

@app.route('/stats', methods=['GET','POST'])
def fetch_slice_stats():
	rgs = req.json
	dset_id = rgs.pop('dset_id')
	svy_id = rgs.pop('svy_id')
	svy = st.dset[dset_id].surveys[svy_id]
	res = svy.fetch_stats_for_slice(**rgs)
	return jsonify(res)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7788, debug=True)
