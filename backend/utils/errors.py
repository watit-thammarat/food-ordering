from rest_framework import status
from rest_framework.response import Response


NAME_IS_REQUIRED = {
    'message': 'Name is required',
    'status': status.HTTP_400_BAD_REQUEST
}

MENU_IS_DUPLICATED = {
    'message': 'Menu is duplicated',
    'status': status.HTTP_400_BAD_REQUEST
}

USER_IS_DUPLICATED = {
    'message': 'User is duplicated',
    'status': status.HTTP_400_BAD_REQUEST
}

EMAIL_IS_REQUIRED = {
    'message': 'Email is required',
    'status': status.HTTP_400_BAD_REQUEST
}

PASSWORD_IS_REQUIRED = {
    'message': 'Pasword is required',
    'status': status.HTTP_400_BAD_REQUEST
}

INVALID_DATE = {
    'message': 'Invalid date',
    'status': status.HTTP_400_BAD_REQUEST
}

INVALID_ORDER_DATE = {
    'message': 'Invalid order date',
    'status': status.HTTP_400_BAD_REQUEST
}

INVALID_MENU_ID = {
    'message': 'Invalid menu id',
    'status': status.HTTP_400_BAD_REQUEST
}

AUTHENTICATION_FAILURE = {
    'message': 'Invalid username and/or password',
    'status': status.HTTP_401_UNAUTHORIZED
}

INVALID_ADMIN = {
    'message': 'Invalid administrator',
    'status': status.HTTP_401_UNAUTHORIZED
}

RESOURCE_NOT_FOUND = {
    'message': 'Resource not found',
    'status': status.HTTP_404_NOT_FOUND
}

INTERNAL_SERVER_ERROR = {
    'message': 'Internal Server Error',
    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
}
