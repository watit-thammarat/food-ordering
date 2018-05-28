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

menu_not_found = {
    'message': 'Menu not found',
    'status': status.HTTP_404_NOT_FOUND
}

internal_server_error = {
    'message': 'Internal Server Error',
    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
}
