import django.shortcuts

import aggregator.models
import aggregator.parsers.controller


def index(request):
    schedule = aggregator.models.Schedule.objects.all()
    return django.shortcuts.render(
        request, 'www/index.html', {'schedule': schedule})


def tag(request, pk):
    t = aggregator.models.Tag.objects.get(pk=pk)
    return django.shortcuts.render(
        request, 'www/tag.html', {'tag': t})


def events_list(request):
    events = aggregator.models.Event.objects.all()
    return django.shortcuts.render(
        request, 'www/events_list.html', {'events': events})


def event(request, pk):
    e = aggregator.models.Event.objects.get(pk=pk)
    return django.shortcuts.render(
        request, 'www/event.html', {'event': e})


def places_list(request):
    places = aggregator.models.Place.objects.all()
    return django.shortcuts.render(
        request, 'www/places_list.html', {'places': places})


def place(request, pk):
    p = aggregator.models.Place.objects.get(pk=pk)
    return django.shortcuts.render(
        request, 'www/place.html', {'place': p})


def run_parsers(request):
    statuses = aggregator.parsers.controller.Controller.run()
    return django.shortcuts.render(
        request, 'www/run_parsers.html', {'statuses': statuses})
