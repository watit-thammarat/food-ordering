from rest_framework.views import exception_handler

from food_ordering.settings import DEBUG
from orders.utils.http_exception import HttpException
from orders.utils import errors


def custom_exception_handler(exception, context):
    if isinstance(exception, HttpException):
        return exception.get_response()
    if not DEBUG:
        return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()
    return exception_handler(exc, context)
