from .base import *


# Secret Settings

DEBUG = False

ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS")


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/debug.log'),
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/info.log'),
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/warning.log'),
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/error.log'),
        },
        'critical': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/critical.log'),
        },
        'mail_admins': {
            'level': 'INFO',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'task': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/task.log'),
        }
    },
    'loggers': {
        'django': {
            'handlers': ['debug', 'info', 'warning', 'error', 'critical', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'background_tasks': {
            'handlers': ['task'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}
