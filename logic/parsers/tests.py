import datetime
import xml.etree.ElementTree

import django.test

import core.models
import logic.parsers.kudago


class KudaGoParserTests(django.test.TestCase):
    xml_events = """
    <events>
    <event id="12345" price="true" type="doo">
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
    <place id="54321" type="other">
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
    <session date="2016-03-20" event="12345" place="54321" time="20:00"/>
    </schedule>
    """

    def test__event(self):
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        </feed>
        """.format(self.xml_events)
        root = xml.etree.ElementTree.fromstring(xml_data)
        events = root.findall('events/event')
        logic.parsers.kudago.Parser.process_event(events[0])
        #
        e = core.models.Event.objects.filter(ext_id=12345).first()
        #
        self.assertEqual(e.type, core.models.EventType.unknown)
        self.assertEqual(e.title, 'Moo')
        self.assertEqual(e.description, '')
        self.assertEqual(e.text, 'loo')
        self.assertEqual(e.age_restrictions, 99)
        #
        t = core.models.Tag.objects.filter(tag='foo').first()
        et = e.eventtags_set.filter(tag_id=t.id).first()
        self.assertEqual(et.tag.tag, 'foo')
        #
        ei = e.eventimages_set.filter(image='boo.png').first()
        self.assertEqual(ei.event.id, e.id)
        #
        ed = e.eventdata_set.filter(key='head.price').first()
        self.assertEqual(ed.value, 'true')

    def test_place(self):
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        </feed>
        """.format(self.xml_places)
        root = xml.etree.ElementTree.fromstring(xml_data)
        places = root.findall('places/place')
        logic.parsers.kudago.Parser.process_place(places[0])
        #
        p = core.models.Place.objects.filter(ext_id=54321).first()
        #
        self.assertEqual(p.type, core.models.PlaceType.other)
        self.assertEqual(p.title, 'Place 16')
        self.assertEqual(p.text, 'Hey!')
        self.assertEqual(p.url, 'http://www.ya.ru/')
        self.assertEqual(p.address, 'outer space')
        self.assertEqual(p.geo_latitude, 59.9)
        self.assertEqual(p.geo_longitude, 30.3)
        #
        city = core.models.City.objects.filter(name='SPB').first()
        self.assertEqual(p.city_id, city.id)
        #
        t = core.models.Tag.objects.filter(tag='Ship').first()
        pt = p.placetags_set.filter(tag_id=t.id).first()
        self.assertEqual(pt.tag.tag, 'Ship')
        #
        pp = p.placephones_set.filter(type=core.models.PhoneType.other).first()
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

    def test__schedule(self):
        xml_data = """<?xml version="1.0" encoding="utf8"?>
        <feed version="1.1">
        {}
        {}
        {}
        </feed>
        """.format(self.xml_events, self.xml_places, self.xml_schedulers)
        root = xml.etree.ElementTree.fromstring(xml_data)
        events = root.findall('events/event')
        logic.parsers.kudago.Parser.process_event(events[0])
        places = root.findall('places/place')
        logic.parsers.kudago.Parser.process_place(places[0])
        sessions = root.findall('schedule/session')
        logic.parsers.kudago.Parser.process_schedule(sessions[0])
        #
        e = core.models.Event.objects.filter(ext_id=12345).first()
        p = core.models.Place.objects.filter(ext_id=54321).first()
        s = core.models.Schedule.objects.filter(event_id=e.id, place_id=p.id).first()
        #
        self.assertEqual(s.date, datetime.date(2016, 3, 20))
        self.assertEqual(s.start_time, datetime.time(20, 0))
        self.assertEqual(s.end_time, None)
