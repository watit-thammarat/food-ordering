from django.conf.urls import url, include
from django.contrib import admin

from orders.views import home, catch_all


urlpatterns = [
    url(r'^$', home),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('orders.urls')),
    url(r'(?P<path>.*)', catch_all),
]
