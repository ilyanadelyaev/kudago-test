import os

import django.http


__test_data = None


def test_data(request):
    global __test_data
    if __test_data is None:
        cur_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(cur_path, 'data.xml')) as f:
            __test_data = f.read()

    return django.http.HttpResponse(__test_data, content_type='application/xml')
