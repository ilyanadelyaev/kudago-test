import os

import django.http


class XMLRender(object):
    __rss_xml_kudago = None

    @classmethod
    def rss_xml_kudago(cls, request):
        if cls.__rss_xml_kudago is None:
            cur_path = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(cur_path, 'kudago.xml')) as f:
                cls.__rss_xml_kudago = f.read()
        return django.http.HttpResponse(cls.__rss_xml_kudago, content_type='application/xml')
