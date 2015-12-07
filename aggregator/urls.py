from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('aggregator.www.urls', namespace='www')),
    url(r'^rss/', include('aggregator.rss.urls', namespace='rss')),
]
