import django.conf.urls

import aggregator.rss.views


urlpatterns = [
    django.conf.urls.url(
        r'^xml/kudago/$',
        aggregator.rss.views.XMLRender.xml_kudago,
        name='xml_kudago'
    ),
]
