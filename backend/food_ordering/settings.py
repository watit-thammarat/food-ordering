import os

from food_ordering.constants import DEVELOPMENT, BETA

PYTHON_ENV = os.getenv('PYTHON_ENV') or DEVELOPMENT

if PYTHON_ENV == DEVELOPMENT:
    from food_ordering.dev_settings import *
elif PYTHON_ENV == BETA:
    from food_ordering.beta_setting import *
