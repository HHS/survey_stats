from survey_stats.error import InvalidUsage, EmptyFilterError, ComputationError
from flask import Flask, redirect, g, render_template
from flask import request as req
from flask.json import jsonify

@app.errorhandler(InvalidUsage)
@app.errorhandler(EmptyFilterError)
@app.errorhandler(ComputationError)
def handle_invalid_usage(error):
    bt.send_last_exception(attributes=error.to_dict())
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def fetch(err=None):
    return redirect('/apidocs/index.html')

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

