from icalendar import Calendar
import dateutil
import datetime
from django.utils import timezone
import pytz


class VEvent():
    uid = '' #uuid
    created = '' #datetime
    summary = '' #string
    sequence = 0 #int
    dtend = '' #datetime
    last_modified = '' #datetime
    dtstart = '' #datetime
    location = ''
    description = ''
    recurrences =  []
    all_day = True


    @property
    def duration(self):
        """
        Return timedelta
        """
        return self.dtend - self.dtstart

    @staticmethod
    def parse(source):
        event = VEvent()
        event.uid = str(source.get('uid'))
        event.summary = str(source.get('summary'))
        event.created = source.get('created').dt
        event.sequence = source.get('sequence')
        event.dtstart = source.get('dtstart').dt
        event.dtend = source.get('dtend').dt
        event.description = source.get('description')
        event.location = source.get('location')
        if source.get('recurrence-id'):
            event.dtstart = source.get('recurrence-id').dt
        if source.get('duration'):
            event.dtend = event.dtstart + source.get('duration').td
        tz = pytz.timezone('Europe/Berlin')
        if hasattr(event.dtstart, 'tzinfo'):
            tz = event.dtstart.tzinfo
            event.dtstart = event.dtstart.replace(tzinfo=None)
            event.all_day = False

        rule = dateutil.rrule.rruleset()
        if source.get('rrule'):
            rrule = source.get('rrule').to_ical().decode('utf-8')
            rule.rrule(dateutil.rrule.rrulestr(rrule,
                dtstart=event.dtstart, ignoretz=True))
        if source.get('rdate'):
            for date in source.get('rdate').dts:
                dt = date.dt
                if hasattr(dt, 'tzinfo'):
                    dt = dt.replace(tzinfo=None)
                rule.rdate(dt)
        if source.get('exrule'):
            exrule = source.get('exrule').to_ical().decode('utf-8')
            rule.exrule(dateutil.rrule.rrulestr(exrule,
                dtstart=event.dtstart, ignoretz=True))
        if source.get('exdate'):
            for date in source.get('exdate').dts:
                dt = date.dt
                if hasattr(dt, 'tzinfo'):
                    dt = dt.replace(tzinfo=None)
                rule.exdate(dt)
        event.last_modified = source.get('last-modified').dt

        event.recurrences = set(list(rule))
        event.recurrences.discard(event.dtstart)
        event.recurrences = [tz.localize(r) for r in event.recurrences]
        if hasattr(event.dtstart, 'tzinfo'):
            event.dtstart = tz.localize(event.dtstart)
        return event


def parse_ical(data):
    cal = Calendar.from_ical(data)
    events = []
    for event in cal.walk('vevent'):
        events.append(VEvent.parse(event))
    return events

