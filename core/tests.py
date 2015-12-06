import uuid
import random
import datetime

import django.test

import core.models


class ModelTests(django.test.TestCase):
    @staticmethod
    def _random_time():
        dt = datetime.datetime.utcfromtimestamp(random.randint(0, 86400))
        return datetime.time(hour=dt.hour, minute=dt.minute, second=dt.second)

    @staticmethod
    def _random_date():
        return datetime.date.today() + \
            datetime.timedelta(days=random.randint(0, 100))

    @staticmethod
    def _tag():
        tg = str(uuid.uuid4())
        t = core.models.Tag(tag=tg)
        t.save()
        return t.id, tg

    @staticmethod
    def _event():
        ex = str(uuid.uuid4())
        ty = core.models.EventType.other
        tl = str(uuid.uuid4())
        dc = str(uuid.uuid4()) * 5
        tt = str(uuid.uuid4()) * 10
        ar = 100
        e = core.models.Event(
            ext_id=ex,
            type=ty,
            title=tl,
            description=dc,
            text=tt,
            age_restrictions=ar,
        )
        e.save()
        return e.id, ex, ty, tl, dc, tt, ar

    @staticmethod
    def _city():
        nm = str(uuid.uuid4())
        c = core.models.City(name=nm)
        c.save()
        return c.id, nm

    @classmethod
    def _place(cls):
        ex = str(uuid.uuid4())
        ty = core.models.PlaceType.other
        tl = str(uuid.uuid4())
        tt = str(uuid.uuid4()) * 10
        ur = str(uuid.uuid4()) * 2
        cid, _ = cls._city()
        ct = core.models.City.objects.get(id=cid)
        ad = str(uuid.uuid4()) * 4
        la = float(random.randrange(-90.0, 90.0))
        lo = float(random.randrange(-180.0, 180.0))
        p = core.models.Place(
            ext_id=ex,
            type=ty,
            title=tl,
            text=tt,
            url=ur,
            city=ct,
            address=ad,
            geo_latitude=la,
            geo_longitude=lo
        )
        p.save()
        return p.id, ex, ty, tl, tt, ur, cid, ad, la, lo

    @classmethod
    def _schedule(cls):
        eid, _, _, _, _, _, _ = cls._event()
        e = core.models.Event.objects.get(id=eid)
        pid, _, _, _, _, _, _, _, _, _ = cls._place()
        p = core.models.Place.objects.get(id=pid)
        dt = cls._random_date()
        st = cls._random_time()
        et = cls._random_time()
        s = core.models.Schedule(
            event=e, place=p,
            date=dt, start_time=st, end_time=et
        )
        s.save()
        return s.id, eid, pid, dt, st, et

    def test__tag(self):
        tid, tg = self._tag()
        t = core.models.Tag.objects.get(id=tid)
        self.assertEqual(t.tag, tg)

    def test__event(self):
        eid, ex, ty, tl, dc, tt, ar = self._event()
        e = core.models.Event.objects.get(id=eid)
        self.assertEqual(e.ext_id, ex)
        self.assertEqual(e.type, ty)
        self.assertEqual(e.title, tl)
        self.assertEqual(e.description, dc)
        self.assertEqual(e.text, tt)
        self.assertEqual(e.age_restrictions, ar)

    def test__event_tags(self):
        eid, _, _, _, _, _, _ = self._event()
        tid, _ = self._tag()
        e = core.models.Event.objects.get(id=eid)
        t = core.models.Tag.objects.get(id=tid)
        e.eventtags_set.create(tag=t)
        et = core.models.EventTags.objects.get(event_id=eid, tag_id=tid)
        self.assertEqual(et.event_id, eid)
        self.assertEqual(et.tag.tag, t.tag)

    def test__event_images(self):
        eid, _, _, _, _, _, _ = self._event()
        im = str(uuid.uuid4()) * 5
        e = core.models.Event.objects.get(id=eid)
        e.eventimages_set.create(image=im)
        ei = core.models.EventImages.objects.get(event_id=eid)
        self.assertEqual(ei.image, im)

    def test__event_data(self):
        eid, _, _, _, _, _, _ = self._event()
        k = str(uuid.uuid4())
        v = str(uuid.uuid4()) * 5
        e = core.models.Event.objects.get(id=eid)
        e.eventdata_set.create(key=k, value=v)
        ed = core.models.EventData.objects.get(event_id=eid, key=k)
        self.assertEqual(ed.key, k)
        self.assertEqual(ed.value, v)

    def test__city(self):
        cid, nm = self._city()
        c = core.models.City.objects.get(id=cid)
        self.assertEqual(c.name, nm)

    def test__place(self):
        pid, ex, ty, tl, tt, ur, cid, ad, la, lo = self._place()
        p = core.models.Place.objects.get(id=pid)
        self.assertEqual(p.ext_id, ex)
        self.assertEqual(p.type, ty)
        self.assertEqual(p.title, tl)
        self.assertEqual(p.text, tt)
        self.assertEqual(p.url, ur)
        self.assertEqual(p.city_id, cid)
        self.assertEqual(p.address, ad)
        self.assertEqual(p.geo_latitude, la)
        self.assertEqual(p.geo_longitude, lo)

    def test__place_tags(self):
        pid, _, _, _, _, _, _, _, _, _ = self._place()
        tid, _ = self._tag()
        p = core.models.Place.objects.get(id=pid)
        t = core.models.Tag.objects.get(id=tid)
        p.placetags_set.create(tag=t)
        pt = core.models.PlaceTags.objects.get(place_id=pid, tag_id=tid)
        self.assertEqual(pt.place_id, pid)
        self.assertEqual(pt.tag.tag, t.tag)

    def test__place_phones(self):
        pid, _, _, _, _, _, _, _, _, _ = self._place()
        pt = core.models.PhoneType.other
        ph = str(uuid.uuid4())
        p = core.models.Place.objects.get(id=pid)
        p.placephones_set.create(type=pt, phone=ph)
        pp = core.models.PlacePhones.objects.get(place_id=pid, type=pt)
        self.assertEqual(pp.phone, ph)

    def test__place_metros(self):
        pid, _, _, _, _, _, _, _, _, _ = self._place()
        ms = str(uuid.uuid4()) * 2
        p = core.models.Place.objects.get(id=pid)
        p.placemetros_set.create(metro=ms)
        pm = core.models.PlaceMetros.objects.get(place_id=pid)
        self.assertEqual(pm.metro, ms)

    def test__place_work_times(self):
        pid, _, _, _, _, _, _, _, _, _ = self._place()
        ty = core.models.WorkTimeType.openhours
        wt = str(uuid.uuid4()) * 3
        p = core.models.Place.objects.get(id=pid)
        p.placeworktimes_set.create(type=ty, work_time=wt)
        pw = core.models.PlaceWorkTimes.objects.get(place_id=pid, type=ty)
        self.assertEqual(pw.work_time, wt)

    def test__place_images(self):
        pid, _, _, _, _, _, _, _, _, _ = self._place()
        im = str(uuid.uuid4()) * 5
        p = core.models.Place.objects.get(id=pid)
        p.placeimages_set.create(image=im)
        pi = core.models.PlaceImages.objects.get(place_id=pid)
        self.assertEqual(pi.image, im)

    def test__place_data(self):
        pid, _, _, _, _, _, _, _, _, _ = self._place()
        k = str(uuid.uuid4())
        v = str(uuid.uuid4()) * 5
        p = core.models.Place.objects.get(id=pid)
        p.placedata_set.create(key=k, value=v)
        pd = core.models.PlaceData.objects.get(place_id=pid, key=k)
        self.assertEqual(pd.key, k)
        self.assertEqual(pd.value, v)

    def test__schedule(self):
        sid, eid, pid, dt, st, et = self._schedule()
        s = core.models.Schedule.objects.get(id=sid)
        self.assertEqual(s.event_id, eid)
        self.assertEqual(s.place_id, pid)
        self.assertEqual(s.date, dt)
        self.assertEqual(s.start_time, st)
        self.assertEqual(s.end_time, et)
