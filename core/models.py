import django.db.models

import core.tools.enum


class Tag(django.db.models.Model):
    tag = django.db.models.CharField(max_length=40)


####################


class EventType(core.tools.enum.Enum):
    unknown = 0
    other = 1

    _choices = (
        (unknown, 'unknown'),
        (other, 'other'),
    )


class Event(django.db.models.Model):
    feed_id = django.db.models.PositiveIntegerField()
    type = django.db.models.PositiveSmallIntegerField(
        choices=EventType())
    #
    title = django.db.models.CharField(max_length=100)
    description = django.db.models.TextField()
    text = django.db.models.TextField()
    #
    age_restrictions = django.db.models.PositiveSmallIntegerField()


class EventTags(django.db.models.Model):
    """
    to search via tags
    """
    event = django.db.models.ForeignKey(Event)
    tag = django.db.models.ForeignKey(Tag)


class EventPersons(django.db.models.Model):
    event = django.db.models.ForeignKey(Event)
    name = django.db.models.CharField(max_length=50)
    role = django.db.models.CharField(max_length=50)


class EventImages(django.db.models.Model):
    event = django.db.models.ForeignKey(Event)
    image = django.db.models.CharField(max_length=100)


class EventData(django.db.models.Model):
    """
    mics keys in events
    """
    event = django.db.models.ForeignKey(Event)
    key = django.db.models.CharField(max_length=20)
    value = django.db.models.CharField(max_length=100)


####################


class PlaceType(core.tools.enum.Enum):
    unknown = 0
    other = 1

    _choices = (
        (unknown, 'unknown'),
        (other, 'other'),
    )


class City(django.db.models.Model):
    name = django.db.models.CharField(max_length=30)


class Place(django.db.models.Model):
    feed_id = django.db.models.PositiveIntegerField()
    type = django.db.models.PositiveSmallIntegerField(
        choices=PlaceType())
    #
    title = django.db.models.CharField(max_length=100)
    text = django.db.models.TextField()
    #
    url = django.db.models.CharField(max_length=250)
    #
    city = django.db.models.ForeignKey(City)
    address = django.db.models.CharField(max_length=200)
    geo_latitude = django.db.models.FloatField()
    geo_longitude = django.db.models.FloatField()


class PlaceTags(django.db.models.Model):
    place = django.db.models.ForeignKey(Place)
    tag = django.db.models.ForeignKey(Tag)



class PhoneType(core.tools.enum.Enum):
    unknown = 0
    other = 1

    _choices = (
        (unknown, 'unknown'),
        (other, 'other'),
    )


class PlacePhones(django.db.models.Model):
    place = django.db.models.ForeignKey(Place)
    type = django.db.models.PositiveSmallIntegerField(
        choices=PhoneType())
    phone = django.db.models.CharField(max_length=20)


class PlaceMetros(django.db.models.Model):
    place = django.db.models.ForeignKey(Place)
    metro = django.db.models.CharField(max_length=30)


class WorkTimeType(core.tools.enum.Enum):
    unknown = 0
    other = 1
    openhours = 2
    kassa = 3

    _choices = (
        (unknown, 'unknown'),
        (other, 'other'),
        (openhours, 'openhours'),
        (kassa, 'kassa'),
    )


class PlaceWorkTimes(django.db.models.Model):
    place = django.db.models.ForeignKey(Place)
    type = django.db.models.PositiveSmallIntegerField(
        choices=WorkTimeType())
    work_time = django.db.models.CharField(max_length=50)


class PlaceImages(django.db.models.Model):
    place = django.db.models.ForeignKey(Place)
    image = django.db.models.CharField(max_length=100)


class PlaceData(django.db.models.Model):
    """
    misc keys in places
    """
    place = django.db.models.ForeignKey(Place)
    key = django.db.models.CharField(max_length=20)
    value = django.db.models.CharField(max_length=100)


####################


class Schedule(django.db.models.Model):
    event = django.db.models.ForeignKey(Event)
    place = django.db.models.ForeignKey(Place)
    #
    date = django.db.models.DateField()
    start_time = django.db.models.TimeField()
    end_time = django.db.models.TimeField()
