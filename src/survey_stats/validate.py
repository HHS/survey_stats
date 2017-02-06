from webargs import fields, ValidationError
from webargs.flaskparser import use_args, use_kwargs

class SurveyYearValidator(BaseConverter):
    """
    year(int) for which survey data is available.
    """

    def to_python(self, value):
        if not int(value) in apst['yrbss'].survey_years:
            raise ValueError('Selected year is not available!' + \
                             ' Choose from: %s' % str(apst['yrbss'].survey_years))
        return int(value)


    def to_url(self, value):
        return BaseConverter.to_url(str(value))

def validated_facet(f):
    if not User.query.get(val):
        # Optionally pass a status_code
        raise ValidationError('User does not exist')


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

