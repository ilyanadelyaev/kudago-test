import django.db.models


class Event(django.db.models.Model):
    age_restrictions = django.db.models.CharField(max_length=4)  # 100+
    title = django.db.models.CharField(max_length=60)
    description = django.db.models.TextField()
    text = django.db.models.TextField()


class Tag(django.db.models.Model):
    tag = django.db.models.CharField(max_length=40)


class EventTags(django.db.models.Model):
    """
    to search via tags
    """
    event = django.db.models.ForeignKey(Event)
    tag = django.db.models.ForeignKey(Tag)


class EventPersons(django.db.models.Model):
    event = django.db.models.ForeignKey(Event)
    name = django.db.models.CharField(max_length=60)
    role = django.db.models.CharField(max_length=30)


class EventImages(django.db.models.Model):
    event = django.db.models.ForeignKey(Event)
    image = django.db.models.CharField(max_length=100)  # maybe ImageField


class EventData(django.db.models.Model):
    """
    other keys in events
    """
    event = django.db.models.ForeignKey(Event)
    key = django.db.models.CharField(max_length=20)
    value = django.db.models.CharField(max_length=100)


####################


class Place(django.db.models.Model):
    pass


####################


class Schedule(django.db.models.Model):
    pass
