from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from order.models import Menu
from shared import errors
from shared.http_exception import HttpException


class MenuList(APIView):
    def post(self, request):
        try:
            name = request.data.get('name')
            if name is None or len(name) == 0:
                raise HttpException(errors.name_is_required)
            count = Menu.objects.filter(name=name).count()
            if count > 0:
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
        except Exception:
            return HttpException(errors.internal_server_error).getResponse()


class MenuDetail(APIView):
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
            name = request.data.get('name')
            if name is None or len(name) == 0:
                raise HttpException(errors.name_is_required)
            count = Menu.objects.filter(~Q(id=id), name=name).count()
            if count > 0:
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
            menu = self.get_object(id)
            menu.delete()
            return Response({'data': 'OK'}, status=status.HTTP_200_OK)
        except HttpException as e:
            return e.getResponse()
        except Exception:
            return HttpException(errors.internal_server_error).getResponse()
