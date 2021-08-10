import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'pipeline': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'exchange_data.log'),
            'mode': 'a',
            'formatter': 'default',
            "encoding": "utf-8",
        },
    },
    'loggers': {
        'pipeline': {
            'handlers': ['pipeline'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}