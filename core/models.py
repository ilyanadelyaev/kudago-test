import django.db.models

import core.tools.enum


class Tag(django.db.models.Model):
    """
    Tags for events and places
    """
    tag = django.db.models.CharField(max_length=40)

    def __unicode__(self):
        return self.tag


####################


class EventType(core.tools.enum.Enum):
    """
    Event type enum to compact type field
    Please update manually
    Unknown types will store in EventData
    """
    unknown = 0
    other = 1

    _choices = (
        (unknown, 'unknown'),
        (other, 'other'),
    )


class Event(django.db.models.Model):
    """
    Base event model

    ext_id: PARSER:EXTERNAL_ID string
    """
    ext_id = django.db.models.CharField(db_index=True, max_length=100)
    type = django.db.models.PositiveSmallIntegerField(
        choices=EventType())
    #
    title = django.db.models.CharField(max_length=100)
    description = django.db.models.TextField()
    text = django.db.models.TextField()
    #
    age_restrictions = django.db.models.PositiveSmallIntegerField(
        null=True, blank=True)

    def type_str(self):
        """
        type to str via EventType
        """
        return EventType(self.type)

    def __unicode__(self):
        return '[{} : {}] ({}) {}'.format(
            self.id, self.ext_id, self.type, self.title)


class EventTags(django.db.models.Model):
    """
    Search events via tags
    """
    event = django.db.models.ForeignKey(Event)
    tag = django.db.models.ForeignKey(Tag)

    def __unicode__(self):
        return '[{}] {}'.format(
            self.event.id, self.tag.tag)


class EventImages(django.db.models.Model):
    """
    Store all event images links here
    """
    event = django.db.models.ForeignKey(Event)
    image = django.db.models.CharField(max_length=100)

    def __unicode__(self):
        return '[{}] {}'.format(
            self.event.id, self.image)


class EventData(django.db.models.Model):
    """
    Unknown event data
    Do not miss anything
    """
    event = django.db.models.ForeignKey(Event)
    key = django.db.models.CharField(max_length=20)
    value = django.db.models.CharField(max_length=100)

    def __unicode__(self):
        return '[{}] {} = {}'.format(
            self.event.id, self.key, self.value)


####################


class PlaceType(core.tools.enum.Enum):
    """
    Place type enum to compact type field
    Please update manually
    Unknown types will store in PlaceData
    """
    unknown = 0
    other = 1

    _choices = (
        (unknown, 'unknown'),
        (other, 'other'),
    )


class City(django.db.models.Model):
    """
    Keep city unque and compact storage
    """
    name = django.db.models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Place(django.db.models.Model):
    """
    Base place model

    ext_id: PARSER:EXTERNAL_ID string
    """
    ext_id = django.db.models.CharField(db_index=True, max_length=100)
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
    geo_latitude = django.db.models.FloatField(null=True)
    geo_longitude = django.db.models.FloatField(null=True)

    def type_str(self):
        """
        type to str via PlaceType
        """
        return PlaceType(self.type)

    def __unicode__(self):
        return '[{} : {}] ({}) {}'.format(
            self.id, self.ext_id, self.type, self.title)


class PlaceTags(django.db.models.Model):
    """
    Search places via tags
    """
    place = django.db.models.ForeignKey(Place)
    tag = django.db.models.ForeignKey(Tag)

    def __unicode__(self):
        return '[{}] {}'.format(
            self.place.id, self.tag.tag)


class PhoneType(core.tools.enum.Enum):
    """
    Phone type enum to compact type field
    Please update manually
    Unknown types will store in PlaceData
    """
    unknown = 0
    other = 1

    _choices = (
        (unknown, 'unknown'),
        (other, 'other'),
    )


class PlacePhones(django.db.models.Model):
    """
    One place may have multiple phones
    """
    place = django.db.models.ForeignKey(Place)
    type = django.db.models.PositiveSmallIntegerField(
        choices=PhoneType())
    phone = django.db.models.CharField(max_length=20)

    def __unicode__(self):
        return '[{}] ({}) {}'.format(
            self.place.id, self.type, self.phone)


class PlaceMetros(django.db.models.Model):
    """
    One place may be located near multiple metro stations
    """
    place = django.db.models.ForeignKey(Place)
    metro = django.db.models.CharField(max_length=30)

    def __unicode__(self):
        return '[{}] {}'.format(
            self.place.id, self.metro)


class WorkTimeType(core.tools.enum.Enum):
    """
    Work time type enum to compact type field
    Please update manually
    Unknown types will store in PlaceData
    """
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
    """
    Working time by type
    For example "open hours" or "ticket office work"
    """
    place = django.db.models.ForeignKey(Place)
    type = django.db.models.PositiveSmallIntegerField(
        choices=WorkTimeType())
    work_time = django.db.models.CharField(max_length=50)

    def __unicode__(self):
        return '[{}] ({}) {}'.format(
            self.place.id, self.type, self.work_time)


class PlaceImages(django.db.models.Model):
    """
    Store all place images links here
    """
    place = django.db.models.ForeignKey(Place)
    image = django.db.models.CharField(max_length=100)

    def __unicode__(self):
        return '[{}] {}'.format(
            self.place.id, self.image)


class PlaceData(django.db.models.Model):
    """
    misc keys in places
    """
    place = django.db.models.ForeignKey(Place)
    key = django.db.models.CharField(max_length=20)
    value = django.db.models.CharField(max_length=100)

    def __unicode__(self):
        return '[{}] {} = {}'.format(
            self.place.id, self.key, self.value)


####################


class Schedule(django.db.models.Model):
    """
    Event time and place
    """
    event = django.db.models.ForeignKey(Event)
    place = django.db.models.ForeignKey(Place)
    #
    date = django.db.models.DateField()
    start_time = django.db.models.TimeField(null=True, blank=True)
    end_time = django.db.models.TimeField(null=True, blank=True)

    def __unicode__(self):
        return '[{}] {} / {} : {} {}'.format(
            self.id,
            self.event.id, self.place.id,
            self.date, self.start_time)
