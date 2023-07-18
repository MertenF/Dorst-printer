import logging
from logging.config import dictConfig

from flask.logging import default_handler

dictConfig(
    {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            },
            'log_file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': 'dorst-printer.log',
                'maxBytes': 10000,
                'backupCount': 10,
                'delay': 'True',
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'email', 'log_file']
        }
    }
)

