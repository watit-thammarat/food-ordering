from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db import transaction
from django.db.models import Q, Count, F
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

from orders import view_models
from orders.models import Menu, Order
from orders.utils import errors, validator, auth
from orders.utils.logger import Logger
from orders.utils.http_exception import HttpException

AVAILABLE_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTION', 'HEAD']


@api_view(AVAILABLE_METHODS)
@permission_classes((AllowAny,))
def home(request):
    response = Response({'data': 'Food Ordering Application'})
    response['Cache-Control'] = 'max-age=600'
    return response


@api_view(AVAILABLE_METHODS)
@permission_classes((AllowAny,))
def catch_all(request, path):
    response = HttpException(errors.RESOURCE_NOT_FOUND).get_response()
    response['Cache-Control'] = 'max-age=600'
    return response


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
        response = Response({'data': view_models.get_order(order)})
        response['Cache-Control'] = 'max-age=0, must-revalidate'
        return response
    except HttpException as e:
        return e.get_response()
    except Exception as e:
        Logger.log_exception(e)
        return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def get_order_summary(request, timestamp):
    try:
        order_date = validator.get_date_from_timestamp(timestamp)
        orders = Order.objects.filter(order_date=order_date).values(
            'menu__id', 'menu__name').annotate(
                total=Count('menu__id')).order_by('total')
        response = Response({'data': view_models.get_order_summary(orders)})
        response['Cache-Control'] = 'max-age=8'
        return response
    except HttpException as e:
        return e.get_response()
    except Exception as e:
        Logger.log_exception(e)
        return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_order(request, timestamp):
    try:
        order_date = validator.get_date_from_timestamp(timestamp)
        user_id = request.user.id
        orders = Order.objects.select_related('menu').filter(
            order_date=order_date, user_id=user_id)
        if len(orders) > 1:
            raise HttpException(errors.INVALID_ORDER)
        data = None if len(orders) == 0 else view_models.get_order(orders[0])
        response = Response({'data': data})
        response['Cache-Control'] = 'max-age=8'
        return response
    except HttpException as e:
        return e.get_response()
    except Exception as e:
        Logger.log_exception(e)
        return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()


@api_view(['POST'])
def sigin(request):
    try:
        email, password = validator.validate_sign_up_sign_in_fields(request)
        user = authenticate(username=email, password=password)
        if user is None:
            raise HttpException(errors.AUTHENTICATION_FAILURE)
        user_logged_in.send(sender=user.__class__,
                            request=request, user=user)
        response = Response({'data': auth.create_jwt(user)})
        response['Cache-Control'] = 'max-age=0, must-revalidate'
        return response
    except HttpException as e:
        return e.get_response()
    except Exception as e:
        Logger.log_exception(e)
        return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()


@api_view(['POST'])
def sigup(request):
    try:
        email, password = validator.validate_sign_up_sign_in_fields(request)
        if User.objects.filter(username=email).count() > 0:
            raise HttpException(errors.USER_IS_DUPLICATED)
        user = User.objects.create_user(
            username=email, email=email, password=password)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        data = {'data': auth.create_jwt(user)}
        response = Response(data, status=status.HTTP_201_CREATED)
        response['Cache-Control'] = 'max-age=0, must-revalidate'
        return response
    except HttpException as e:
        return e.get_response()
    except Exception as e:
        Logger.log_exception(e)
        return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()


class MenuList(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            validator.validate_admin(request)
            name = validator.validate_menu_name_field(request)
            if Menu.objects.filter(name=name).count() > 0:
                raise HttpException(errors.MENU_IS_DUPLICATED)
            Menu.objects.create(name=name)
            response = Response({'data': 'OK'}, status=status.HTTP_201_CREATED)
            response['Cache-Control'] = 'max-age=0, must-revalidate'
            return response
        except HttpException as e:
            return e.get_response()
        except Exception as e:
            Logger.log_exception(e)
            return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()

    def get(self, request):
        try:
            menu_list = Menu.objects.all()
            response = Response({'data': view_models.get_menu_list(menu_list)})
            response['Cache-Control'] = 'max-age=8'
            return response
        except Exception as e:
            Logger.log_exception(e)
            return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()


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
            response = Response({'data': view_models.get_menu(menu)})
            response['Cache-Control'] = 'max-age=8'
            return response
        except HttpException as e:
            return e.get_response()
        except Exception as e:
            Logger.log_exception(e)
            return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()

    def put(self, request, id):
        try:
            validator.validate_admin(request)
            name = validator.validate_menu_name_field(request)
            if Menu.objects.filter(~Q(id=id), name=name).count() > 0:
                raise HttpException(errors.MENU_IS_DUPLICATED)
            menu = self.get_object(id)
            menu.name = name
            menu.save()
            response = Response({'data': view_models.get_menu(menu)})
            response['Cache-Control'] = 'max-age=0, must-revalidate'
            return response
        except HttpException as e:
            return e.get_response()
        except Exception as e:
            Logger.log_exception(e)
            return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()

    def delete(self, request, id):
        try:
            validator.validate_admin(request)
            menu = self.get_object(id)
            menu.delete()
            response = Response({'data': 'OK'})
            response['Cache-Control'] = 'max-age=0, must-revalidate'
            return response
        except HttpException as e:
            return e.get_response()
        except Exception as e:
            Logger.log_exception(e)
            return HttpException(errors.INTERNAL_SERVER_ERROR).get_response()
