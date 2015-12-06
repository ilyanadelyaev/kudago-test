import django.conf.urls

import aggregator.rssrender.views


urlpatterns = [
    django.conf.urls.url(
        r'^xml/kudago/$',
        aggregator.rssrender.views.XMLRender.rss_xml_kudago,
        name='rss_xml_kudago'
    ),
]
