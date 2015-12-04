from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('www.urls', namespace='www')),

    url(r'^admin/', include(admin.site.urls)),
]
