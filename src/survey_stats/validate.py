from webargs import fields
import webargs
from webargs.core import Parser
from survey_stats import state as st
from werkzeug.routing import BaseConverter

p = Parser()

stats_args = {
    'q': fields.Str(required=True)

}

"""
    qn = req.args.get('q')
    vars = [] if not 'v' in req.args else req.args.get('v').split(',')
    resp = True if not 'r' in req.args else not 0 ** int(req.args.get('r'),2)
    filt = {} if not 'f' in req.args else dict(
        map(lambda fv: (fv.split(':')[0],
                        fv.split(':')[1].split(',')),
            req.args.get('f').split(';')))
    logging.info(filt)

"""

class SurveyYearValidator(BaseConverter):
    """
    year(int) for which survey data is available.
    """

    def to_python(self, value):
        if not int(value) in yrbss.survey_years:
            raise ValueError('Selected year is not available!' + \
                             ' Choose from: %s' % str(st.survey['yrbss'].survey_years))
        return int(value)


    def to_url(self, value):
        return BaseConverter.to_url(str(value))
