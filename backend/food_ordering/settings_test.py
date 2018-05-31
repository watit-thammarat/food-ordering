import os

from food_ordering.settings_common import *


SECRET_KEY = 'zjc_5+kf1p2ryhp5e_&3epabc7@x(zh$*vk@e013toc%3vkeg^'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

JWT_AUTH['JWT_SECRET_KEY'] = SECRET_KEY

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True
}
