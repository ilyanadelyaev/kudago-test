import django.shortcuts

import core.models
import parsers.controller


def index(request):
    schedule = core.models.Schedule.objects.all()
    return django.shortcuts.render(request, 'www/index.html', {'schedule': schedule})


def tag(request, pk):
    tag = core.models.Tag.objects.get(pk=pk)
    return django.shortcuts.render(request, 'www/tag.html', {'tag': tag})


def events_list(request):
    events = core.models.Event.objects.all()
    return django.shortcuts.render(request, 'www/events_list.html', {'events': events})


def event(request, pk):
    event = core.models.Event.objects.get(pk=pk)
    return django.shortcuts.render(request, 'www/event.html', {'event': event})


def places_list(request):
    places = core.models.Place.objects.all()
    return django.shortcuts.render(request, 'www/places_list.html', {'places': places})


def place(request, pk):
    place = core.models.Place.objects.get(pk=pk)
    return django.shortcuts.render(request, 'www/place.html', {'place': place})


def run_parsers(request):
    statuses = parsers.controller.Controller.run()
    return django.shortcuts.render(request, 'www/run_parsers.html', {'statuses': statuses})
