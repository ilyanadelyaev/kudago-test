import django.conf.urls

import aggregator.www.views


urlpatterns = [
    django.conf.urls.url(
        r'^$',
        aggregator.www.views.index, name='index'),

    django.conf.urls.url(
        r'^tag/(?P<pk>[0-9]+)/$',
        aggregator.www.views.tag, name='tag'),
    django.conf.urls.url(
        r'^event/(?P<pk>[0-9]+)/$',
        aggregator.www.views.event, name='event'),
    django.conf.urls.url(
        r'^event/$',
        aggregator.www.views.events_list, name='events_list'),
    django.conf.urls.url(
        r'^place/(?P<pk>[0-9]+)/$',
        aggregator.www.views.place, name='place'),
    django.conf.urls.url(
        r'^place/$',
        aggregator.www.views.places_list, name='places_list'),

    django.conf.urls.url(
        r'^run_parsers$',
        aggregator.www.views.run_parsers, name='run_parsers'),
]
