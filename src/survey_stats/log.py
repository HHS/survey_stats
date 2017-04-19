import socket
import traceback
import logging
from logging.handlers import SysLogHandler
from werkzeug.routing import BaseConverter

from survey_stats import settings

class ContextFilter(logging.Filter):

  def filter(self, record):
    return True

def getLogger(name='survey_stat_deflog'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(syslog)
    logger.addHandler(errlog)
    f = ContextFilter()
    logger.addFilter(f)
    return logger

formatter = logging.Formatter(
    '%(asctime)s - STATS: %(message)s',
    datefmt='%b %d %H:%M:%S'
)
errlog = logging.StreamHandler()
errlog.setFormatter(formatter)
syslog = SysLogHandler(address=('logs5.papertrailapp.com', 16468))
syslog.setFormatter(formatter)

logger = getLogger()
