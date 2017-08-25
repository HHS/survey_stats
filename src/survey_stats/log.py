import logging.config
import structlog

timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
pre_chain = [
	# Add the log level and a timestamp to the event_dict if the log entry
	# is not from structlog.
	structlog.stdlib.add_log_level,
	timestamper,
]

logging.config.dictConfig({
	"version": 1,
	"disable_existing_loggers": False,
	"formatters": {
		"plain": {
			"()": structlog.stdlib.ProcessorFormatter,
			"processor": structlog.dev.ConsoleRenderer(colors=False),
			"foreign_pre_chain": pre_chain,
		},
		"colored": {
			"()": structlog.stdlib.ProcessorFormatter,
			"processor": structlog.dev.ConsoleRenderer(colors=True),
			"foreign_pre_chain": pre_chain,
		},
	},
	"handlers": {
		"default": {
			"level": "DEBUG",
			"class": "logging.StreamHandler",
			"formatter": "colored",
		},
		"file": {
			"level": "INFO",
			"class": "logging.handlers.WatchedFileHandler",
			"filename": "test.log",
			"formatter": "plain",
		},
	},
	"loggers": {
		"": {
			"handlers": ["default", "file"],
			"level": "INFO",
			"propagate": True,
		},
	}
})

structlog.configure(
	processors=[
		structlog.stdlib.add_log_level,
		timestamper,
		structlog.processors.StackInfoRenderer(),
		structlog.processors.format_exc_info,
		#structlog.processors.JSONRenderer(),
		structlog.processors.KeyValueRenderer(key_order=['event','level'])
	],
	context_class=structlog.threadlocal.wrap_dict(dict),
	logger_factory=structlog.stdlib.LoggerFactory(),
	wrapper_class=structlog.stdlib.BoundLogger,
	cache_logger_on_first_use=True,
)

def getLogger(name='surveystats-default-log'):
	return structlog.get_logger(name)
