import django.conf.urls

import www.views


urlpatterns = [
    django.conf.urls.url(r'^$', www.views.index, name='index'),

    django.conf.urls.url(r'^event/(?P<pk>[0-9]+)/$', www.views.event, name='event'),
    django.conf.urls.url(r'^event/$', www.views.events_list, name='events_list'),
    django.conf.urls.url(r'^place/(?P<pk>[0-9]+)/$', www.views.place, name='place'),
    django.conf.urls.url(r'^place/$', www.views.places_list, name='places_list'),

    django.conf.urls.url(r'^run_parsers$', www.views.run_parsers, name='run_parsers'),
]
