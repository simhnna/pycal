import datetime
import calendar

from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
import pytz

from pycal.models.events import Event, get_next_events

def home(request):
    events = get_next_events(request, 10)
    return render(request, 'home.html',
                  {'events': events,
                   'home': True,
                   })


def feed(request):
    return render(request, 'feed.html')

def calendar_view(request, year, month):
    year = int(year)
    month = int(month)

    prev_month = month - 1
    next_month = month + 1
    prev_year = year
    next_year = year
    today = timezone.now().day

    if prev_month == 0:
        prev_month = 12
        prev_year -= 1
    elif next_month == 13:
        next_month = 1
        next_year += 1

    last_day = calendar.monthrange(year, month)[-1]
    first_week_day = datetime.date(year, month, 1).weekday()
    last_week_day = datetime.date(year, month, last_day).weekday()

    current_month = timezone.now().month

    events = []

    next_link = reverse('calendar_specific', args=(next_year, next_month))
    prev_link = reverse('calendar_specific', args=(prev_year, prev_month))

    if month < 1 or month > 12:
        raise Http404(_("Invalid Date"))
    date_end = pytz.timezone('utc').localize(
        datetime.datetime(next_year, next_month, 1, 0, 0, 0))
    date_start = pytz.timezone('utc').localize(
        datetime.datetime(year, month, 1, 0, 0, 0))

    all_events = Event.objects.filter(Q(dtstart__gte=date_start), Q(dtstart__lt=date_end))
    if request.user.is_authenticated():
        all_events = all_events.filter(
                Q(group__id__in=request.user.groups.values_list('id', flat=True))
                | Q(group__isnull=True))
    else:
        all_events = all_events.filter(Q(group__isnull=True))

    # add empty days
    for i in range(0, first_week_day):
        events.append(CalendarDay(
            calendar.monthrange(prev_year, prev_month)[-1] + 1 - first_week_day + i,
            current_month=False)
            )

    counter = first_week_day
    for i in range(1, last_day + 1):
        current_day= datetime.date(year, month, i)
        e = all_events.filter(Q(dtstart__day=i)|Q(dtstart__lt=current_day, dtend__gt=current_day))
        day = CalendarDay(i)
        if i == today and current_month == month and year == timezone.now().year:
            day.today = True
        day.events = e
        if counter == 6:
            counter = -1
            day.sunday = True
        events.append(day)
        counter += 1

    # add empty days
    counter = 1
    for i in range(last_week_day, 6):
        events.append(CalendarDay(counter, current_month=False))
        counter += 1

    return render(request, 'index.html',
                  {'days': events,
                   'day_names': [_(day) for day in calendar.day_name],
                   'year': year,
                   'month': _(datetime.date(year, month, 1).strftime('%B')),
                   'next_link': next_link,
                   'prev_link': prev_link,
                   'calendar': True,
                   }
                  )


class CalendarDay:
    events = []
    sunday = False
    today = False

    def __init__(self, day, current_month=True):
        self.current_month = current_month
        self.day = day

    def is_current(self):
        return self.day != -1
