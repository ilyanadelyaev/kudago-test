from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('aggregator.urls', namespace='aggregator')),
    url(r'^admin/', include(admin.site.urls)),
]
