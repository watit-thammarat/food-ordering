from rest_framework import status
from rest_framework.response import Response

from orders.utils.logger import Logger
from orders.utils.errors import INTERNAL_SERVER_ERROR as ERROR


class AppException(Exception):
    def __init__(self, error):
        super().__init__(error['message'])
        self.message = error['message']
        self.status = error['status']

    @staticmethod
    def get_response(ex):
        if isinstance(ex, AppException):
            response = Response({'detail': ex.message}, status=ex.status)
        else:
            Logger.log_exception(ex)
            response = Response(
                {'detail': ERROR['message']}, status=ERROR['status'])
        response['Cache-Control'] = 'max-age=0, must-revalidate'
        return response
