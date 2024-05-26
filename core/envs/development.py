import logging
import os
import sys

import sentry_sdk
from django.utils.log import DEFAULT_LOGGING
from sentry_sdk.integrations.django import DjangoIntegration

from .common import *
from ..libs.logging import LogInfo

DEBUG = True

ENVIRONMENT = "dev"

"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}
"""
LOG_BASE_DIR = os.path.join(BASE_DIR, 'logs')
LOGLEVEL = "ERROR"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "filters": {
        "hide_phone": {
            "()": "core.libs.logging.PhoneNumberFilter",
            "display_digits": 10 if ENVIRONMENT == "dev" else 4,
        },
    },
    'formatters': {
        # 'default': {
        #     'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        # },
        # 'console': {
        #     'format': '%(name)-12s %(levelname)-8s %(message)s'
        # },
        'standard': {
            "class": "logging.Formatter",
            # 'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
            "format": "[%(asctime)-10s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            # "datefmt": "%d/%b/%Y %H:%M:%S",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
        "file": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
            "format": "%(asctime)s %(msecs)03d %(levelname)s %(name)s %(lineno)s %(message)s",
        },
        "json": {
            "()": "core.libs.logging.MyJSONFormatter",
            "fmt_keys": {
                "level": "levelname",
                "message": "message",
                "timestamp": "timestamp",
                "logger": "name",
                "module": "module",
                "function": "funcName",
                "line": "lineno",
                "thread_name": "threadName"
            }
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {

        # # Rotaton logs by timeing every midnight it check old backup file and if it reachs to 7 it will remove the oldest one
        # 'file': {
        #     'class': 'logging.handlers.TimedRotatingFileHandler',
        #     'filename': 'app.log',
        #     'when': 'midnight',
        #     'interval': 1,
        # 'mode': 'a',
        #     'backupCount': 7,
        # },
        #
        # # Rotaion logs by file limit size 1 MB and max 5 files
        # 'file': {
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': 'app.log',
        #     'maxBytes': 1024 * 1024,  # 1 MB
        # 'mode': 'a',
        #     'backupCount': 5,
        # },
        #
        # # Use sentry logging handler here
        # 'sentry': {
        #     'level': 'WARNING',
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        # },

        'console': {
            'class': 'logging.StreamHandler',
            # "class": "rich.logging.RichHandler",
            'formatter': 'standard'
        },
        'file_safe': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'json',
            'mode': 'a',
            "encoding": "utf8",
            "filters": ["hide_phone"],
            # 'filename': '/tmp/debug.log'
            'filename': os.path.join(LOG_BASE_DIR, 'app_safe.jsonl'),
        },
        'file_error': {
            'level': LOGLEVEL,
            'class': 'logging.FileHandler',
            'formatter': 'json',
            # 'filename': '/tmp/debug.log'
            'mode': 'a',
            "encoding": "utf8",
            "filters": ["hide_phone"],
            'filename': os.path.join(LOG_BASE_DIR, 'app_error.jsonl'),
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],

    },
    'loggers': {
        '': {
            'handlers': ['console', 'file_safe', 'file_error'],
            # 'level': LOGLEVEL,
            'propagate': True,
        },
        'django_logging': {
            'handlers': ['console', 'file_safe', 'file_error'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],

        # use raven as sentry template in django
        # 'app': {
        #     'level': LOGLEVEL,
        #     'handlers': ['console', 'file', 'sentry'],
        #     'propagate': False,
        # },
    },
}

# Logging config for sentry and raven
LOGGING_ = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {
        "level": "DEBUG",
        "handlers": ["sentry"],
    },
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        'sentry': {
            "level": "WARNING",
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console"],
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        'proj_djsentry': {  # <= base Project
            'level': 'WARNING',
            'handlers': ['console', 'sentry'],
            # required to avoid double logging with root logger
            'propagate': False,
        },
        'raven': {
            'level': 'WARNING',
            'handlers': ['console', ],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'app_base': {  # <= module name
            'level': 'WARNING',
            'handlers': ['sentry'],
            'propagate': False,
        },
    },
}

# TOKEN_SENTRY = os.environ.get('TOKEN_SENTRY')
# sentry_sdk.init(
#     dsn=TOKEN_SENTRY,
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     traces_sample_rate=1.0,
#     # Set profiles_sample_rate to 1.0 to profile 100%
#     # of sampled transactions.
#     # We recommend adjusting this value in production.
#     profiles_sample_rate=1.0,
#     integrations=[DjangoIntegration()],
#     send_default_pii = True,
# )
# Logging config for sentry and raven
# Add token that identifies the sentry project
# RAVEN_CONFIG = {}
# if TOKEN_SENTRY:
#     sentry_sdk.init(
#         dsn=TOKEN_SENTRY,
#         integrations=[DjangoIntegration()],
#         traces_sample_rate=1.0,
#         send_default_pii=True
#     )
#     RAVEN_CONFIG = {
#         "dsn": TOKEN_SENTRY,
#     }
