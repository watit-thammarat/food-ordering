from rest_framework import status
from rest_framework.response import Response


name_is_required = {
    'message': 'Name is required',
    'status': status.HTTP_400_BAD_REQUEST
}

menu_is_duplicated = {
    'message': 'Menu is duplicated',
    'status': status.HTTP_400_BAD_REQUEST
}

user_is_duplicated = {
    'message': 'User is duplicated',
    'status': status.HTTP_400_BAD_REQUEST
}

email_is_required = {
    'message': 'Email is required',
    'status': status.HTTP_400_BAD_REQUEST
}

password_is_required = {
    'message': 'Pasword is required',
    'status': status.HTTP_400_BAD_REQUEST
}

invalid_date = {
    'message': 'Invalid date',
    'status': status.HTTP_400_BAD_REQUEST
}

invalid_order_date = {
    'message': 'Invalid order date',
    'status': status.HTTP_400_BAD_REQUEST
}

invalid_menu_id = {
    'message': 'Invalid menu id',
    'status': status.HTTP_400_BAD_REQUEST
}

authentication_failure = {
    'message': 'Invalid username and/or password',
    'status': status.HTTP_401_UNAUTHORIZED
}

invalid_admin = {
    'message': 'Invalid administrator',
    'status': status.HTTP_401_UNAUTHORIZED
}

internal_server_error = {
    'message': 'Internal Server Error',
    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
}
