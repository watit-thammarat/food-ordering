from rest_framework import status
from rest_framework.response import Response


class HttpException(Exception):
    def __init__(self, error):
        self.message = error['message']
        self.status = error['status']

    def get_response(self):
        return Response({'detail': self.message}, status=self.status)
