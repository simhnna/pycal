from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm
from django import forms
from django.http import HttpResponse
from django.utils import timezone
from calendar import monthrange
from events.models import Event
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

import datetime
import pytz


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.POST['next'])
    else:
        return render(request, 'set_timezone.html', {'timezones': pytz.common_timezones}) 

def home(request):
    events = Event.get_next_events(10)

    return render(request, 'home.html',
            {'events': events,
                'home': True,
                })
def calendar(request, year, month):
    year = int(year)
    month = int(month)

    all_events = Event.objects.filter(start_date__year=year,
            start_date__month=month)
    last_day = monthrange(year, month)[-1]
    first_week_day = datetime.date(year, month, 1).weekday()
    last_week_day = datetime.date(year, month, last_day).weekday()
    day_names = [_('Monday'), _('Tuesday'), _('Wednesday'), _('Thursday'), _('Friday'), _('Saturday'), _('Sunday')]
    
    current_month = timezone.now().month

    events = []

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

    next_link = reverse('calendar_specific', args=(next_year, next_month))
    prev_link = reverse('calendar_specific', args=(prev_year, prev_month))


    # add empty days
    for i in range(0, first_week_day):
        events.append(CalendarDay(monthrange(prev_year, prev_month)[-1] + 1 - first_week_day + i,
            current_month=False))

    counter = first_week_day
    for i in range(1, last_day + 1):
        e = all_events.filter(start_date__day=i)
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
                'day_names': day_names,
                'year': year,
                'month': _(datetime.date(year, month, 1).strftime('%B')),
                'next_link': next_link,
                'prev_link': prev_link,
                'calendar': True,
                })



class CalendarDay():
    events = []
    sunday = False
    today = False

    def __init__(self, day, current_month=True):
        self.current_month = current_month
        self.day = day

    def is_current(self):
        return self.day != -1
