import uuid

import django.test

import core.models


class _BaseModelTests(django.test.TestCase):
    @staticmethod
    def _event():
        ar = '100+'
        tl = str(uuid.uuid4())
        dc = str(uuid.uuid4()) * 5
        tt = str(uuid.uuid4()) * 10
        e = core.models.Event(age_restrictions=ar, title=tl, description=dc, text=tt)
        e.save()
        return e, ar, tl, dc, tt

    @staticmethod
    def _tag():
        tg = str(uuid.uuid4())
        t = core.models.Tag(tag=tg)
        t.save()
        return t, tg


class EventModelTests(_BaseModelTests):
    def test__has_fields(self):
        _, ar, tl, dc, tt = self._event()
        e = core.models.Event.objects.get(title=tl)
        self.assertEqual(e.age_restrictions, ar)
        self.assertEqual(e.title, tl)
        self.assertEqual(e.description, dc)
        self.assertEqual(e.text, tt)


class TagModelTests(_BaseModelTests):
    def test__has_fields(self):
        _, tg = self._tag()
        t = core.models.Tag.objects.get(tag=tg)
        self.assertEqual(t.tag, tg)


class EventTagsModelTests(_BaseModelTests):
    def test__has_fields(self):
        e, _, _, _, _ = self._event()
        t, _ = self._tag()
        e.eventtags_set.create(tag=t)
        et = core.models.EventTags.objects.get(event_id=e.id, tag_id=t.id)
        self.assertEqual(et.event.id, e.id)


class EventPersonsModelTests(_BaseModelTests):
    def test__has_fields(self):
        e, _, _, _, _ = self._event()
        pn = str(uuid.uuid4())
        pr = str(uuid.uuid4())
        e.eventpersons_set.create(name=pn, role=pr)
        ep = core.models.EventPersons.objects.get(event_id=e.id, name=pn)
        self.assertEqual(ep.name, pn)
        self.assertEqual(ep.role, pr)


class EventImagesModelTests(_BaseModelTests):
    def test__has_fields(self):
        e, _, _, _, _ = self._event()
        im = str(uuid.uuid4()) * 5
        e.eventimages_set.create(image=im)
        ei = core.models.EventImages.objects.get(event_id=e.id, image=im)
        self.assertEqual(ei.image, im)


class EventDataModelTests(_BaseModelTests):
    def test__has_fields(self):
        e, _, _, _, _ = self._event()
        k = str(uuid.uuid4())
        v = str(uuid.uuid4()) * 5
        e.eventdata_set.create(key=k, value=v)
        ed = core.models.EventData.objects.get(event_id=e.id, key=k)
        self.assertEqual(ed.key, k)
        self.assertEqual(ed.value, v)


class PlaceModelTests(_BaseModelTests):
    def test__has_fields(self):
        pass


class ScheduleModelTests(_BaseModelTests):
    def test__has_fields(self):
        pass
