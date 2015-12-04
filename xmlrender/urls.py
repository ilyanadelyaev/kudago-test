import django.conf.urls

import xmlrender.views


urlpatterns = [
    django.conf.urls.url(r'^test_data/$', xmlrender.views.test_data, name='test_data'),
]
