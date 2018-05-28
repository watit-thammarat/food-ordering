from django.conf.urls import url
from orders.views import sigin, sigup, make_order, MenuList, MenuDetail

urlpatterns = [
    url(r'^sign-in$', sigin),
    url(r'^sign-up$', sigup),
    url(r'^order$', make_order),
    url(r'^menu$', MenuList.as_view()),
    url(r'^menu/(?P<id>[0-9]+)$', MenuDetail.as_view()),
]
