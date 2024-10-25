import os

base_dir = os.path.dirname(os.path.dirname(__file__))

LOG_CONFIG = {
	'version': 1,
	'formatters': {
		'standard': {
			'format': '%(levelname)s [%(asctime)s] %(name)s: %(message)s',
			'datefmt': '%d.%m.%Y %H:%M:%S'
		},
		'simple': {
			'format': '%(levelname)s: %(message)s'
		}
	},
	'handlers': {
		'stream_handler': {
			'level': 'INFO',
			'formatter': 'simple',
			'class': 'logging.StreamHandler',
			'stream': 'ext://sys.stdout'
		},
		'file_handler': {
			'level': 'DEBUG',
			'formatter': 'standard',
			'class': 'logging.FileHandler',
			'filename': os.path.join(base_dir, 'bot.log'),
			'mode': 'a'
		}
	},
	'loggers': {
		'logger': {
			'handlers': ['stream_handler', 'file_handler', ],
			'level': 'DEBUG'
		}
	}
}
