from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^menu$', views.MenuList.as_view()),
    url(r'^menu/(?P<id>[0-9]+)$', views.MenuDetail.as_view()),
]
