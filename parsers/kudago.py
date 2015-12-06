import datetime
import xml.etree.ElementTree
import logging

import parsers.root
import core.models


logger = logging.getLogger('apps.parsers.kudago')


class Parser(parsers.root.ParserRoot):
    class EventExists(RuntimeError):
        pass

    class EventNotExists(RuntimeError):
        pass

    class PlaceExists(RuntimeError):
        pass

    class PlaceNotExists(RuntimeError):
        pass

    class ScheduleExists(RuntimeError):
        pass

    ID = 'kudago'
    URL = 'http://127.0.0.1:8000/rss/xml/kudago'

    @staticmethod
    def get_parser():
        return xml.etree.ElementTree.XMLParser(encoding='utf-8')

    @classmethod
    def parse(cls, root):
        events = root.findall('events/event')
        for e in events:
            try:
                cls.process_event(e)
            except Exception as ex:
                logger.error('Cant parse event with "{}"'.format(str(ex)))
                logger.exception(ex)
        #
        places = root.findall('places/place')
        for p in places:
            try:
                cls.process_place(p)
            except Exception as ex:
                logger.error('Cant parse place with "{}"'.format(str(ex)))
                logger.exception(ex)
        #
        sessions = root.findall('schedule/session')
        for s in sessions:
            try:
                cls.process_schedule(s)
            except Exception as ex:
                logger.error('Cant parse schedule with "{}"'.format(str(ex)))
                logger.exception(ex)
        return True

    @classmethod
    def process_event(cls, event):
        e = core.models.Event()
        e_tags = []
        e_images = []
        e_data = []
        # keys
        for k, v in event.items():
            if k == 'id':
                # EXISTS
                ext_id = '{}:{}'.format(cls.ID, v)
                if core.models.Event.objects.filter(ext_id=ext_id).first():
                    raise cls.EventExists('event.ext_id "{}" already exists'.format(ext_id))
                e.ext_id = ext_id
            elif k == 'type':
                tp = core.models.EventType.get_key(v)
                if tp is None:
                    e.type = core.models.EventType.unknown
                    e_data.append(('head.type', v))
                else:
                    e.type = tp
            else:
                e_data.append(('head.{}'.format(k), v))
        # childs
        for el in event:
            if el.tag == 'title':
                e.title = el.text or ''
            elif el.tag == 'description':
                e.description = el.text or ''
            elif el.tag == 'text':
                e.text = el.text or ''
            elif el.tag == 'age_restricted':
                try:
                    e.age_restrictions = int(el.text[:-1])
                except ValueError:
                    e.age_restrictions = None
                    e_data.append(('age_restricted', el.text))
            elif el.tag == 'tags':
                for tag in el:
                    e_tags.append(tag.text)
            elif el.tag == 'gallery':
                for img in el:
                    i = img.get('href')
                    if i:
                        e_images.append(i)
            else:
                rr = cls._process_unknown_element(el)
                e_data.extend(rr)
        #
        e.save()
        #
        for tt in e_tags:
            t = core.models.Tag.objects.filter(tag=tt).first()
            if t is None:
                t = core.models.Tag(tag=tt)
                t.save()
            e.eventtags_set.create(tag=t)
        #
        for im in e_images:
            e.eventimages_set.create(image=im)
        #
        for k, v in e_data:
            e.eventdata_set.create(key=k, value=v)


    @classmethod
    def process_place(cls, place):
        p = core.models.Place()
        p_city = None
        p_tags = []
        p_phones = []
        p_metros = []
        p_work_times = []
        p_images = []
        p_data = []
        # keys
        for k, v in place.items():
            if k == 'id':
                # EXISTS
                ext_id = '{}:{}'.format(cls.ID, v)
                if core.models.Place.objects.filter(ext_id=ext_id).first():
                    raise cls.PlaceExists('place.ext_id "{}" already exists'.format(ext_id))
                p.ext_id = ext_id
            elif k == 'type':
                tp = core.models.PlaceType.get_key(v)
                if tp is None:
                    p.type = core.models.PlaceType.unknown
                    p_data.append(('head.type', v))
                else:
                    p.type = tp
            else:
                p_data.append(('head.{}'.format(k), v))
        # childs
        for el in place:
            if el.tag == 'title':
                p.title = el.text or ''
            elif el.tag == 'text':
                p.text = el.text or ''
            elif el.tag == 'url':
                p.url = el.text or ''
            elif el.tag == 'city':
                p_city = el.text or None
            elif el.tag == 'address':
                p.address = el.text or ''
            elif el.tag == 'coordinates':
                p.geo_latitude = el.get('latitude') or None
                p.geo_longitude = el.get('longitude') or None
            elif el.tag == 'tags':
                for tag in el:
                    p_tags.append(tag.text)
            elif el.tag == 'phones':
                for ch in el:
                    ty = ch.get('type')
                    if ty:
                        ty = core.models.PhoneType.get_key(ty)
                    if not ty:
                        ty = core.models.PhoneType.unknown
                        p_data.append(('phone.type', ch.get('type')))
                    p_phones.append((ty, ch.text))
            elif el.tag == 'metros':
                for ch in el:
                    p_metros.append(ch.text)
            elif el.tag == 'work_times':
                for ch in el:
                    ty = ch.get('type')
                    if ty:
                        ty = core.models.WorkTimeType.get_key(ty)
                    if not ty:
                        ty = core.models.WorkTimeType.unknown
                        p_data.append(('work_time.type', ch.get('type')))
                    p_work_times.append((ty, ch.text))
            elif el.tag == 'gallery':
                for img in el:
                    i = img.get('href')
                    if i:
                        p_images.append(i)
            else:
                rr = cls._process_unknown_element(el)
                p_data.extend(rr)
        #
        ct = core.models.City.objects.filter(name=p_city).first()
        if not ct:
            ct = core.models.City(name=p_city)
            ct.save()
        p.city = ct
        #
        p.save()
        #
        for tt in p_tags:
            t = core.models.Tag.objects.filter(tag=tt).first()
            if t is None:
                t = core.models.Tag(tag=tt)
                t.save()
            p.placetags_set.create(tag=t)
        #
        for ty, ph in p_phones:
            p.placephones_set.create(type=ty, phone=ph)
        #
        for mt in p_metros:
            p.placemetros_set.create(metro=mt)
        #
        for ty, wt in p_work_times:
            p.placeworktimes_set.create(type=ty, work_time=wt)
        #
        for im in p_images:
            p.placeimages_set.create(image=im)
        #
        for k, v in p_data:
            p.placedata_set.create(key=k, value=v)

    @classmethod
    def process_schedule(cls, schedule):
        s = core.models.Schedule()
        for k, v in schedule.items():
            if k == 'event':
                ext_id = '{}:{}'.format(cls.ID, v)
                e = core.models.Event.objects.filter(ext_id=ext_id).first()
                if not e:
                    raise cls.EventNotExists('event.ext_id "{}" not exists'.format(ext_id))
                s.event_id = e.id
            elif k == 'place':
                ext_id = '{}:{}'.format(cls.ID, v)
                p = core.models.Place.objects.filter(ext_id=ext_id).first()
                if not p:
                    raise cls.PlaceNotExists('place.ext_id "{}" not exists'.format(ext_id))
                s.place_id = p.id
            elif k == 'date':
                s.date = datetime.datetime.strptime(v, '%Y-%m-%d').date()
            elif k == 'time':
                s.start_time = datetime.datetime.strptime(v, '%H:%M').time()
            elif k == 'timetill':
                s.end_time = datetime.datetime.strptime(v, '%H:%M').time()
            else:
                logger.warning('XML: Unmatched key in schedule item: "{}" = "{}"'.format(k, v))
        ss = core.models.Schedule.objects.filter(
            event=s.event, place=s.place,
            date=s.date,
            start_time=s.start_time, end_time=s.end_time,
        ).first()
        if ss:
            raise cls.ScheduleExists('Schedule for event "{}" and place "{}" on "{} {}" exists'.format(
                s.event.ext_id, s.place.ext_id, s.date, s.start_time))
        s.save()
