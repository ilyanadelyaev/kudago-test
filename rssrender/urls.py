import django.conf.urls

import rssrender.views


urlpatterns = [
    django.conf.urls.url(r'^xml/kudago/$', rssrender.views.XMLRender.rss_xml_kudago, name='rss_xml_kudago'),
]
