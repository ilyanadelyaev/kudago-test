import django.shortcuts


def index(request):
    return django.shortcuts.render(request, 'www/index.html')


def run_parsers(request):
    return django.shortcuts.render(request, 'www/run_parsers.html')
