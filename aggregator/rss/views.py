import os

import django.http


class XMLRender(object):
    __xml_kudago = None

    @classmethod
    def xml_kudago(cls, _):
        """
        Fake feed to test KUDAGO parser
        Read data file once
        """
        if cls.__xml_kudago is None:
            cur_path = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
            with open(os.path.join(cur_path, 'static', 'kudago.xml')) as f:
                cls.__xml_kudago = f.read()
        return django.http.HttpResponse(
            cls.__xml_kudago, content_type='application/xml')
