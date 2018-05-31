from food_ordering.settings_common import *
from food_ordering.constants import APP_LOG
from food_ordering.ec2 import get_linux_ec2_private_ip

PRIVATE_IP = get_linux_ec2_private_ip()

LOG_LEVEL = os.getenv('LOG_LEVEL') or 'INFO'

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [
    'food-ordering-beta.ap-southeast-1.elasticbeanstalk.com',
    'localhost',
    '.dekdurian.com'
]

if PRIVATE_IP:
    ALLOWED_HOSTS.append(PRIVATE_IP)

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

JWT_AUTH['JWT_SECRET_KEY'] = SECRET_KEY

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
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'app_logfile': {
            'level': LOG_LEVEL,
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/app.log',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'level': LOG_LEVEL,
            'handlers': ['app_logfile'],
        },
        'py.warnings': {
            'level': LOG_LEVEL,
            'handlers': ['app_logfile'],
        },
        'django.db.backends': {
            'level': LOG_LEVEL,
            'handlers': ['app_logfile'],
        },
        APP_LOG: {
            'level': LOG_LEVEL,
            'handlers': ['app_logfile'],
        }
    }
}
