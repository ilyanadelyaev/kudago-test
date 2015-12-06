import django.shortcuts

import parsers.controller


def index(request):
    return django.shortcuts.render(request, 'www/index.html')


def run_parsers(request):
    ret = parsers.controller.Controller.run()
    return django.shortcuts.render(request, 'www/run_parsers.html', {'ret': ret})
