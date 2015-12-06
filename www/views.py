import django.shortcuts

import core.models
import parsers.controller


def index(request):
    schedule = core.models.Schedule.objects.all()
    return django.shortcuts.render(request, 'www/index.html', {
        'schedule': schedule,
    })


def events_list(request):
    pass


def event(request, pk):
    pass


def places_list(request):
    pass


def place(request, pk):
    pass


def run_parsers(request):
    ret = parsers.controller.Controller.run()
    return django.shortcuts.render(request, 'www/run_parsers.html', {'ret': ret})
