from django.contrib.auth.models import User, Group
from icalendar import Calendar
from events.models import Event


def import_events_from_ics(filename, username, group_name):
    stream = open(filename, 'r')
    data = stream.read()
    stream.close()

    cal = Calendar.from_ical(data)
    group = Group.objects.get(name=group_name)
    user = User.objects.get(username=username)

    for event in cal.walk('vevent'):
        e = Event()
        e.created_by = user
        e.title = event.get('summary')
        e.start_date = event.get('dtstart').dt
        e.end_date = event.get('dtend').dt
        e.group = group 
        e.save()
