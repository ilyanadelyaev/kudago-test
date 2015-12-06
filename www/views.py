import django.shortcuts

import core.models
import parsers.controller


def index(request):
    schedule = core.models.Schedule.objects.all()
    return django.shortcuts.render(request, 'www/index.html', {
        'schedule': schedule,
    })


def events_list(request):
    events = core.models.Event.objects.all()
    return django.shortcuts.render(request, 'www/events_list.html', {
        'events': events,
    })


def event(request, pk):
    pass


def places_list(request):
    places = core.models.Place.objects.all()
    return django.shortcuts.render(request, 'www/places_list.html', {
        'places': places,
    })


def place(request, pk):
    pass


def run_parsers(request):
    ret = parsers.controller.Controller.run()
    return django.shortcuts.render(request, 'www/run_parsers.html', {'ret': ret})
