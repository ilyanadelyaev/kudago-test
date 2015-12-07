1. settings.py - INSTALLED_APPS

INSTALLED_APPS = (
    ...
    'aggregator',
    ...
)


2. settings.py - LOGGING

LOGGING = {
    'formatters': {
        ...
        'verbose': {
            'format':
            "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt':
            "%Y/%m/%d %H:%M:%S"
        },
        ...
    },
    'handlers': {
        ...
        'aggregator': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/aggregator.log',
            'formatter': 'verbose'
        },
        ...
    },
    'loggers': {
        ...
        'aggregator': {
            'handlers': ['aggregator'],
            'level': 'DEBUG',
        },
        ...
    }
}


3. urls.py

urlpatterns = [
    ...
    url(r'^', include('aggregator.urls', namespace='aggregator')),
    ...
]


4. ./sh/init.sh

5. ./sh/run.sh
