from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

from orders import view_models
from orders.models import Menu, Order
from utils import errors, validator, auth
from utils.http_exception import HttpException

AVAILABLE_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTION']


@api_view(AVAILABLE_METHODS)
@permission_classes((AllowAny,))
def home(request):
    return Response({'data': 'Food Ordering Application'})


@api_view(AVAILABLE_METHODS)
@permission_classes((AllowAny,))
def catch_all(request, path):
    return HttpException(errors.RESOURCE_NOT_FOUND).getResponse()


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def make_order(request):
    try:
        order_date = validator.validate_order_date(request)
        menu_id = validator.validate_menu_id(request)
        user_id = request.user.id
        if Menu.objects.filter(id=menu_id).count() == 0:
            raise HttpException(errors.INVALID_MENU_ID)
        with transaction.atomic():
            Order.objects.filter(order_date=order_date,
                                 user_id=user_id, menu_id=menu_id).delete()
            order = Order.objects.create(
                order_date=order_date, user_id=user_id, menu_id=menu_id)
        return Response({'data': view_models.get_order(order)})
    except HttpException as e:
        return e.getResponse()
    except Exception:
        return HttpException(errors.INTERNAL_SERVER_ERROR).getResponse()


@api_view(['POST'])
def sigin(request):
    try:
        email, password = validator.validate_sign_up_sign_in_fields(request)
        user = authenticate(username=email, password=password)
        if user is None:
            raise HttpException(errors.AUTHENTICATION_FAILURE)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return Response({'data': auth.create_jwt(user)})
    except HttpException as e:
        return e.getResponse()
    except Exception:
        return HttpException(errors.INTERNAL_SERVER_ERROR).getResponse()


@api_view(['POST'])
def sigup(request):
    try:
        email, password = validator.validate_sign_up_sign_in_fields(request)
        if User.objects.filter(username=email).count() > 0:
            raise HttpException(errors.USER_IS_DUPLICATED)
        user = User.objects.create_user(
            username=email, email=email, password=password)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return Response({'data': auth.create_jwt(user)},
                        status=status.HTTP_201_CREATED)
    except HttpException as e:
        return e.getResponse()
    except Exception as e:
        return HttpException(errors.INTERNAL_SERVER_ERROR).getResponse()


class MenuList(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            validator.validate_admin(request)
            name = validator.validate_menu_name_field(request)
            if Menu.objects.filter(name=name).count() > 0:
                raise HttpException(errors.MENU_IS_DUPLICATED)
            Menu.objects.create(name=name)
            return Response({'data': 'OK'}, status=status.HTTP_201_CREATED)
        except HttpException as e:
            return e.getResponse()
        except Exception:
            return HttpException(errors.INTERNAL_SERVER_ERROR).getResponse()

    def get(self, request):
        try:
            menu_list = Menu.objects.all()
            return Response({'data': view_models.get_menu_list(menu_list)})
        except HttpException as e:
            return e.getResponse()
        except Exception:
            return HttpException(errors.INTERNAL_SERVER_ERROR).getResponse()


class MenuDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            menu = Menu.objects.get(id=id)
            return menu
        except Exception:
            raise HttpException(errors.INVALID_MENU_ID)

    def get(self, request, id):
        try:
            menu = self.get_object(id)
            return Response({'data': view_models.get_menu(menu)})
        except HttpException as e:
            return e.getResponse()
        except Exception:
            return HttpException(errors.INTERNAL_SERVER_ERROR).getResponse()

    def put(self, request, id):
        try:
            validator.validate_admin(request)
            name = validator.validate_menu_name_field(request)
            if Menu.objects.filter(~Q(id=id), name=name).count() > 0:
                raise HttpException(errors.MENU_IS_DUPLICATED)
            menu = self.get_object(id)
            menu.name = name
            menu.save()
            return Response({'data': view_models.get_menu(menu)})
        except HttpException as e:
            return e.getResponse()
        except Exception:
            return HttpException(errors.INTERNAL_SERVER_ERROR).getResponse()

    def delete(self, request, id):
        try:
            validator.validate_admin(request)
            menu = self.get_object(id)
            menu.delete()
            return Response({'data': 'OK'})
        except HttpException as e:
            return e.getResponse()
        except Exception:
            return HttpException(errors.INTERNAL_SERVER_ERROR).getResponse()
