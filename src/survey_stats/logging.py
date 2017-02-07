import socket
import backtracepython as bt
import traceback
import logging

from survey_stats import settings


"""
from logging.handlers import SysLogHandler
from werkzeug.routing import BaseConverter
class ContextFilter(logging.Filter):
  hostname = socket.gethostname()

  def filter(self, record):
    record.hostname = self.hostname
    return True
f = ContextFilter()
logger.addFilter(f)

syslog = SysLogHandler(address=('logs5.papertrailapp.com', 16468))
formatter = logging.Formatter('%(asctime)s %(hostname)s STATS: %(message)s', datefmt='%b %d %H:%M:%S')

syslog.setFormatter(formatter)
logger.addHandler(syslog)
"""


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


logger.info("starting survey_stats service")
bt.initialize(endpoint=settings.BACKTRACE_URL,
              token=settings.BACKTRACE_TKN)
logger.info("connected to backtrace, logging exceptions...")
