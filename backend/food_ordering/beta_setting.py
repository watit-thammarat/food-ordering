from food_ordering.common_settings import *

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [
    '172.31.34.225',
    'food-ordering-beta.ap-southeast-1.elasticbeanstalk.com',
    'localhost'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRESQL_DATABASE'),
        'USER': os.getenv('POSTGRESQL_USER'),
        'PASSWORD': os.getenv('POSTGRESQL_PASSWORD'),
        'HOST': os.getenv('POSTGRESQL_HOST'),
        'PORT': os.getenv('POSTGRESQL_PORT'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'formatters': {
        'verbose': {
            'format': '[ %(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'app_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/django_app.log',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'verbose'
        },
        'dba_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/django_dba.log',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'dba': {
            'level': 'DEBUG',
            'handlers': ['dba_logfile'],
        },
        'django': {
            'level': 'DEBUG',
            'handlers': ['app_logfile'],
        }
    }
}
