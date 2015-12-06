import django.conf.urls

import www.views


urlpatterns = [
    django.conf.urls.url(r'^$', www.views.index, name='index'),

    django.conf.urls.url(r'^run_parsers$', www.views.run_parsers, name='run_parsers'),
]
