import os

from food_ordering.constants import DEVELOPMENT, BETA

env = os.getenv('PYTHON_ENV') or DEVELOPMENT

print('==> {}'.format(env))

if env == DEVELOPMENT:
    from food_ordering.dev_settings import *
elif env == BETA:
    from food_ordering.beta_setting import *
