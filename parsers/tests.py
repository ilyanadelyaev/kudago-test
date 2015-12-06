import uuid
import datetime
import xml.etree.ElementTree

import django.test

import core.models
import parsers.kudago


class KudaGoParserTests(django.test.TestCase):
    xml_events = """
    <events>
    <event id="{event}" price="true" type="doo">
      <title><![CDATA[Moo]]></title>
      <age_restricted>99+</age_restricted>
      <tags>
        <tag>foo</tag>
      </tags>
      <gallery>
        <image href="boo.png"/>
      </gallery>
      <text><![CDATA[loo]]></text>
    </event>
    </events>
    """

    xml_places = """
    <places>
    <place id="{place}" type="other">
      <staff>bearded man</staff>
      <city>SPB</city>
      <title>Place 16</title>
      <address>outer space</address>
      <coordinates latitude="59.9" longitude="30.3"/>
      <phones>
        <phone type="other">+7 812 495-68-48</phone>
      </phones>
      <work_times>
        <work_time type="openhours">all night</work_time>
      </work_times>
      <tags>
        <tag>Ship</tag>
      </tags>
      <metros>
        <metro>Nevsky</metro>
      </metros>
      <gallery>
        <image href="river.jpg"/>
      </gallery>
      <text><![CDATA[Hey!]]></text>
      <url>http://www.ya.ru/</url>
    </place>
    </places>
    """

    xml_schedulers = """
    <schedule>
    <session date="2016-03-20" event="{event}" place="{place}" time="20:00"/>
    </schedule>
    """

    def test__event(self):
        event_ext_id = str(uuid.uuid4())
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        </feed>
        """.format(self.xml_events.format(event=event_ext_id))
        #
        root = xml.etree.ElementTree.fromstring(xml_data)
        events = root.findall('events/event')
        parsers.kudago.Parser.process_event(events[0])
        #
        ext_id = '{}:{}'.format(parsers.kudago.Parser.ID, event_ext_id)
        e = core.models.Event.objects.get(ext_id=ext_id)
        #
        self.assertEqual(e.type, core.models.EventType.unknown)
        self.assertEqual(e.title, 'Moo')
        self.assertEqual(e.description, '')
        self.assertEqual(e.text, 'loo')
        self.assertEqual(e.age_restrictions, 99)
        #
        t = core.models.Tag.objects.get(tag='foo')
        et = e.eventtags_set.get(tag_id=t.id)
        self.assertEqual(et.tag.tag, 'foo')
        #
        ei = e.eventimages_set.get(image='boo.png')
        self.assertEqual(ei.event.id, e.id)
        #
        ed = e.eventdata_set.get(key='head.price')
        self.assertEqual(ed.value, 'true')

    def test__event__exists(self):
        event_ext_id = str(uuid.uuid4())
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        </feed>
        """.format(self.xml_events.format(event=event_ext_id))
        #
        root = xml.etree.ElementTree.fromstring(xml_data)
        events = root.findall('events/event')
        parsers.kudago.Parser.process_event(events[0])
        #
        with self.assertRaises(parsers.kudago.Parser.EventExists):
            parsers.kudago.Parser.process_event(events[0])

    def test_place(self):
        place_ext_id = str(uuid.uuid4())
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        </feed>
        """.format(self.xml_places.format(place=place_ext_id))
        #
        root = xml.etree.ElementTree.fromstring(xml_data)
        places = root.findall('places/place')
        parsers.kudago.Parser.process_place(places[0])
        #
        ext_id = '{}:{}'.format(parsers.kudago.Parser.ID, place_ext_id)
        p = core.models.Place.objects.get(ext_id=ext_id)
        #
        self.assertEqual(p.type, core.models.PlaceType.other)
        self.assertEqual(p.title, 'Place 16')
        self.assertEqual(p.text, 'Hey!')
        self.assertEqual(p.url, 'http://www.ya.ru/')
        self.assertEqual(p.address, 'outer space')
        self.assertEqual(p.geo_latitude, 59.9)
        self.assertEqual(p.geo_longitude, 30.3)
        #
        city = core.models.City.objects.get(name='SPB')
        self.assertEqual(p.city_id, city.id)
        #
        t = core.models.Tag.objects.get(tag='Ship')
        pt = p.placetags_set.get(tag_id=t.id)
        self.assertEqual(pt.tag.tag, 'Ship')
        #
        pp = p.placephones_set.get(type=core.models.PhoneType.other)
        self.assertEqual(pp.phone, '+7 812 495-68-48')
        #
        pm = p.placemetros_set.filter().first()
        self.assertEqual(pm.metro, 'Nevsky')
        #
        pw = p.placeworktimes_set.filter().first()
        self.assertEqual(pw.type, core.models.WorkTimeType.openhours)
        self.assertEqual(pw.work_time, 'all night')
        #
        pi = p.placeimages_set.filter().first()
        self.assertEqual(pi.image, 'river.jpg')
        #
        pd = p.placedata_set.filter().first()
        self.assertEqual(pd.key, 'staff')
        self.assertEqual(pd.value, 'bearded man')

    def test__place__exists(self):
        place_ext_id = str(uuid.uuid4())
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        </feed>
        """.format(self.xml_places.format(place=place_ext_id))
        #
        root = xml.etree.ElementTree.fromstring(xml_data)
        places = root.findall('places/place')
        parsers.kudago.Parser.process_place(places[0])
        #
        with self.assertRaises(parsers.kudago.Parser.PlaceExists):
            parsers.kudago.Parser.process_place(places[0])

    def test__schedule(self):
        event_ext_id = str(uuid.uuid4())
        place_ext_id = str(uuid.uuid4())
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        {}
        {}
        </feed>
        """.format(
            self.xml_events.format(event=event_ext_id),
            self.xml_places.format(place=place_ext_id),
            self.xml_schedulers.format(event=event_ext_id, place=place_ext_id)
        )
        #
        root = xml.etree.ElementTree.fromstring(xml_data)
        events = root.findall('events/event')
        parsers.kudago.Parser.process_event(events[0])
        places = root.findall('places/place')
        parsers.kudago.Parser.process_place(places[0])
        sessions = root.findall('schedule/session')
        parsers.kudago.Parser.process_schedule(sessions[0])
        #
        ext_id = '{}:{}'.format(parsers.kudago.Parser.ID, event_ext_id)
        e = core.models.Event.objects.get(ext_id=ext_id)
        ext_id = '{}:{}'.format(parsers.kudago.Parser.ID, place_ext_id)
        p = core.models.Place.objects.get(ext_id=ext_id)
        s = core.models.Schedule.objects.get(event_id=e.id, place_id=p.id)
        #
        self.assertEqual(s.date, datetime.date(2016, 3, 20))
        self.assertEqual(s.start_time, datetime.time(20, 0))
        self.assertEqual(s.end_time, None)

    def test__schedule__event_not_exists(self):
        event_ext_id = 0
        place_ext_id = 0
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        {}
        </feed>
        """.format(
            self.xml_places.format(place=place_ext_id),
            self.xml_schedulers.format(event=event_ext_id, place=place_ext_id)
        )
        #
        root = xml.etree.ElementTree.fromstring(xml_data)
        places = root.findall('places/place')
        parsers.kudago.Parser.process_place(places[0])
        sessions = root.findall('schedule/session')
        #
        with self.assertRaises(parsers.kudago.Parser.EventNotExists):
            parsers.kudago.Parser.process_schedule(sessions[0])

    def test__schedule__place_not_exists(self):
        event_ext_id = str(uuid.uuid4())
        place_ext_id = 0
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        {}
        </feed>
        """.format(
            self.xml_events.format(event=event_ext_id),
            self.xml_schedulers.format(event=event_ext_id, place=place_ext_id)
        )
        #
        root = xml.etree.ElementTree.fromstring(xml_data)
        events = root.findall('events/event')
        parsers.kudago.Parser.process_event(events[0])
        sessions = root.findall('schedule/session')
        #
        with self.assertRaises(parsers.kudago.Parser.PlaceNotExists):
            parsers.kudago.Parser.process_schedule(sessions[0])

    def test__schedule__exists(self):
        event_ext_id = str(uuid.uuid4())
        place_ext_id = str(uuid.uuid4())
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        {}
        {}
        </feed>
        """.format(
            self.xml_events.format(event=event_ext_id),
            self.xml_places.format(place=place_ext_id),
            self.xml_schedulers.format(event=event_ext_id, place=place_ext_id)
        )
        #
        root = xml.etree.ElementTree.fromstring(xml_data)
        events = root.findall('events/event')
        parsers.kudago.Parser.process_event(events[0])
        places = root.findall('places/place')
        parsers.kudago.Parser.process_place(places[0])
        sessions = root.findall('schedule/session')
        parsers.kudago.Parser.process_schedule(sessions[0])
        #
        with self.assertRaises(parsers.kudago.Parser.ScheduleExists):
            parsers.kudago.Parser.process_schedule(sessions[0])
