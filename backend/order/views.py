from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from rest_framework_jwt.settings import api_settings

from order.models import Menu
from shared import errors
from shared.http_exception import HttpException

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def is_admin(username):
    user = User.objects.get(username=username)
    return user.is_superuser


def create_jwt(user):
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


def validate_sign_up_sign_in_fields(request):
    email = request.data.get('email')
    if email is None or len(email) == 0:
        raise HttpException(errors.email_is_required)
    password = request.data.get('password')
    if email is None or len(email) == 0:
        raise HttpException(errors.password_is_required)


def validate_menu_name_field(request):
    name = request.data.get('name')
    if name is None or len(name) == 0:
        raise HttpException(errors.name_is_required)


@api_view(['POST'])
def sigin(request):
    try:
        validate_sign_up_sign_in_fields(request)
        user = authenticate(username=email, password=password)
        if user is None:
            raise HttpException(errors.authentication_failure)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return Response({'data': create_jwt(user)}, status=status.HTTP_200_OK)
    except HttpException as e:
        return e.getResponse()
    except Exception:
        return HttpException(errors.internal_server_error).getResponse()


@api_view(['POST'])
def sigup(request):
    try:
        validate_sign_up_sign_in_fields(request)
        if User.objects.filter(username=email).count() > 0:
            raise HttpException(errors.user_is_duplicated)
        user = User.objects.create_user(
            username=email, email=email, password=password)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return Response({'data': create_jwt(user)},
                        status=status.HTTP_201_CREATED)
    except HttpException as e:
        return e.getResponse()
    except Exception as e:
        return HttpException(errors.internal_server_error).getResponse()


class MenuList(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            validate_menu_name_field(request)
            if not is_admin(request.user):
                raise HttpException(errors.invalid_admin)
            if Menu.objects.filter(name=name).count() > 0:
                raise HttpException(errors.menu_is_duplicated)
            Menu.objects.create(name=name)
            return Response({'data': 'OK'}, status=status.HTTP_201_CREATED)
        except HttpException as e:
            return e.getResponse()
        except Exception:
            return HttpException(errors.internal_server_error).getResponse()

    def get(self, request):
        try:
            menus = Menu.objects.all()
            data = []
            for menu in menus:
                data.append({'id': menu.id, 'name': menu.name})
            return Response({'data': data}, status=status.HTTP_200_OK)
        except HttpException as e:
            return e.getResponse()
        except Exception as e:
            print(e)
            return HttpException(errors.internal_server_error).getResponse()


class MenuDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            menu = Menu.objects.get(id=id)
            return menu
        except Menu.DoesNotExist:
            raise HttpException(errors.menu_not_found)

    def get(self, request, id):
        try:
            menu = self.get_object(id)
            data = {'id': menu.id, 'name': menu.name}
            return Response({'data': data}, status=status.HTTP_200_OK)
        except HttpException as e:
            return e.getResponse()
        except Exception:
            return HttpException(errors.internal_server_error).getResponse()

    def put(self, request, id):
        try:
            validate_menu_name_field(request)
            if not is_admin(request.user):
                raise HttpException(errors.invalid_admin)
            if Menu.objects.filter(~Q(id=id), name=name).count() > 0:
                raise HttpException(errors.menu_is_duplicated)
            menu = self.get_object(id)
            menu.name = name
            menu.save()
            data = {'id': menu.id, 'name': menu.name}
            return Response({'data': data}, status=status.HTTP_200_OK)
        except HttpException as e:
            return e.getResponse()
        except Exception:
            return HttpException(errors.internal_server_error).getResponse()

    def delete(self, request, id):
        try:
            if not is_admin(request.user):
                raise HttpException(errors.invalid_admin)
            menu = self.get_object(id)
            menu.delete()
            return Response({'data': 'OK'}, status=status.HTTP_200_OK)
        except HttpException as e:
            return e.getResponse()
        except Exception:
            return HttpException(errors.internal_server_error).getResponse()
