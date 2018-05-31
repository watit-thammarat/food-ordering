from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token
from orders import views

urlpatterns = [
    url(r'^sign-in$', views.sigin),
    url(r'^sign-up$', views.sigup),
    url(r'^token/refresh$', refresh_jwt_token),
    url(r'^orders$', views.make_order),
    url(r'^orders/(?P<timestamp>[0-9]+)/summary$', views.get_order_summary),
    url(r'^orders/(?P<timestamp>[0-9]+)$', views.get_order),
    url(r'^menus$', views.MenuList.as_view()),
    url(r'^menus/(?P<id>[0-9]+)$', views.MenuDetail.as_view()),
    url(r'(?P<path>.*)', views.catch_all),
]
