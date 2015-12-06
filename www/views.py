import django.shortcuts

import core.models
import parsers.controller


def index(request):
    schedule = core.models.Schedule.objects.all()
    return django.shortcuts.render(
        request, 'www/index.html', {'schedule': schedule})


def tag(request, pk):
    t = core.models.Tag.objects.get(pk=pk)
    return django.shortcuts.render(
        request, 'www/tag.html', {'tag': t})


def events_list(request):
    events = core.models.Event.objects.all()
    return django.shortcuts.render(
        request, 'www/events_list.html', {'events': events})


def event(request, pk):
    e = core.models.Event.objects.get(pk=pk)
    return django.shortcuts.render(
        request, 'www/event.html', {'event': e})


def places_list(request):
    places = core.models.Place.objects.all()
    return django.shortcuts.render(
        request, 'www/places_list.html', {'places': places})


def place(request, pk):
    p = core.models.Place.objects.get(pk=pk)
    return django.shortcuts.render(
        request, 'www/place.html', {'place': p})


def run_parsers(request):
    statuses = parsers.controller.Controller.run()
    return django.shortcuts.render(
        request, 'www/run_parsers.html', {'statuses': statuses})
