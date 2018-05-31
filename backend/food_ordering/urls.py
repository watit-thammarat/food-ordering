from django.conf.urls import url, include
from django.contrib import admin

from orders import views as order_views


urlpatterns = [
    url(r'^$', order_views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('orders.urls')),
    url(r'(?P<path>.*)', order_views.catch_all),
]
