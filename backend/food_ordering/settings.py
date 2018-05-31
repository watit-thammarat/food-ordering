import os

from food_ordering.constants import DEVELOPMENT, BETA, TEST

PYTHON_ENV = os.getenv('PYTHON_ENV') or DEVELOPMENT

if PYTHON_ENV == DEVELOPMENT:
    from food_ordering.settings_dev import *
elif PYTHON_ENV == TEST:
    from food_ordering.settings_test import *
elif PYTHON_ENV == BETA:
    from food_ordering.setting_beta import *
