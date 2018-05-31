from rest_framework import status
from rest_framework.response import Response


class HttpException(Exception):
    def __init__(self, error):
        self.message = error['message']
        self.status = error['status']

    def get_response(self):
        response = Response({'detail': self.message}, status=self.status)
        response['Cache-Control'] = 'max-age=0, must-revalidate'
        return response
