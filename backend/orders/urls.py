from django.conf.urls import url
from orders.views import (sigin, sigup, make_order,
                          get_order, MenuList, MenuDetail, get_order_summary)

urlpatterns = [
    url(r'^sign-in$', sigin),
    url(r'^sign-up$', sigup),
    url(r'^orders$', make_order),
    url(r'^orders/(?P<timestamp>[0-9]+)/summary$', get_order_summary),
    url(r'^orders/(?P<timestamp>[0-9]+)$', get_order),
    url(r'^menus$', MenuList.as_view()),
    url(r'^menus/(?P<id>[0-9]+)$', MenuDetail.as_view()),
]
