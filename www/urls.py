import django.conf.urls

import www.views


urlpatterns = [
    django.conf.urls.url(r'^$', www.views.index, name='index'),
]
