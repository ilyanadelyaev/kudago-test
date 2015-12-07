import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    README = f.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='aggregator',
    version='0.01-alpha',
    packages=[
        'aggregator',
        'aggregator.tools',
        'aggregator.parsers',
        'aggregator.www',
        'aggregator.rss',
    ],
    include_package_data=True,
    description='RSS feeds aggregator',
    long_description=README,
    url='https://github.com/ilyanadelyaev/django-aggregator',
    author='Ilya Nadelyaev',
    author_email='nadelyaev.ilya@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
