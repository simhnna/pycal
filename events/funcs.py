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
    rrule = '' # string
    rdate = []
    exrule = '' # string 
    exdate = []  # set of dates
    last_modified = '' #datetime
    dtstart = '' #datetime
    location = ''
    description = ''
    recurrence_id = None
    recurrences =  []


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
        if source.get('duration'):
            event.dtend = event.dtstart + source.get('duration').td

        rule = dateutil.rrule.rruleset()
        if source.get('rrule'):
            event.rrule = source.get('rrule').to_ical().decode('utf-8')
            rule.rrule(dateutil.rrule.rrulestr(event.rrule, dtstart=event.dtstart))
        if source.get('rdate'):
            for date in source.get('rdate').dts:
                rule.rdate(date.dt)
                event.rdate.append(date.dt)
        if source.get('exrule'):
            event.exrule = source.get('exrule').to_ical().decode('utf-8')
            rule.exrule(dateutil.rrule.rrulestr(event.exrule, dtstart=event.dtstart))
        if source.get('exdate'):
            for e in source.get('exdate').dts:
                rule.exdate(e.dt)
                event.exdate.append(e.dt)
        event.last_modified = source.get('last-modified').dt
        if source.get('recurrence-id'):
            event.recurrence_id = source.get('recurrence-id').dt
            event.dtend = event.recurrence_id + event.duration
            event.dtstart = event.recurrence_id

        event.recurrences = set(list(rule))
        event.recurrences.discard(event.dtstart)
        exdates = [e.date() for e in event.exdate]
        to_remove = []
        for rec in event.recurrences:
            if rec.date() in exdates:
                to_remove.append(rec)
        event.recurrences.difference_update(to_remove)
        return event


def parse_ical(data):
    cal = Calendar.from_ical(data)
    events = []
    for event in cal.walk('vevent'):
        events.append(VEvent.parse(event))
    return events

