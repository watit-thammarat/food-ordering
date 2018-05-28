from django.conf.urls import url
from order import views
from order.views import sigin, sigup

urlpatterns = [
    url(r'^sign-in$', sigin),
    url(r'^sign-up$', sigup),
    url(r'^menu$', views.MenuList.as_view()),
    url(r'^menu/(?P<id>[0-9]+)$', views.MenuDetail.as_view()),

]
