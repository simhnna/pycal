from django.db import models
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.db.models import Q

from icalendar import Calendar
import uuid
import urllib.request

from profiles.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = _('Categories')
        verbose_name = _('Category')

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    location = models.CharField(max_length=100, verbose_name=_('Location'))
    description = models.TextField(verbose_name=_('Description'))
    start_date = models.DateTimeField(verbose_name=_('Start'))
    end_date = models.DateTimeField(verbose_name=_('End'), blank=True, null=True)
    all_day = models.BooleanField(default=False)
    details = models.TextField(verbose_name=_('Details'), null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name=_('Group'))
    category = models.ForeignKey(Category, null=True, blank=True)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False)

    class Meta:
        verbose_name_plural = _('Events')
        verbose_name = _('Event')

    def __str__(self):
        return self.title

    def send_email_notifications(self, link):
        users = Profile.objects.filter(email_notifications=True)
        if self.group:
            users = users.filter(user__groups=self.group)
        messages = []
        for u in users:
            if u.user.email != '':
                messages.append((self.title, render_to_string('events/event_notification.txt',
                                                              {'event': self, 'user': u.user,
                                                                  'link': link}),
                                 'pycal@serve-me.info', [u.user.email]))

        send_mass_mail(messages)

    def get_absolute_url(self):
        return reverse('events:detail', args=(self.id,))

    def attendants(self):
        return Attendant.objects.filter(event=self).count()

    def is_attending(self, user):
        if not user.is_anonymous():
            return Attendant.objects.filter(event=self, user=user).exists()


class Attendant(models.Model):
    def __str__(self):
        return '{} is attending {}'.format(self.user, self.event)

    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)

def get_next_events(request, number_of_events):
    now = timezone.now().replace(hour=0, minute=0, second=0)
    events = Event.objects.filter(Q(start_date__gte=now) | Q(start_date__lte=timezone.now(), end_date__gte=timezone.now())).order_by('start_date')
    if request.user.is_authenticated():
        events = events.filter(Q(group__id__in=request.user.groups.values_list('id', flat=True))
                              | Q(group__isnull=True))
    else:
        events = events.exclude(group__isnull=False)
    return events[:number_of_events]


class UUIDMapping(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mapped_string = models.CharField(max_length=120, unique=True, db_index=True)


class RemoteCalendar(models.Model):
    title = models.CharField(max_length=60)
    url = models.URLField()
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)


    def __str__(self):
        return self.title 

    def poll_calendar(self):
        with urllib.request.urlopen(self.url) as response:
            data = response.read()
        return process_ical_events(data, self.user, self.category)


def process_ical_events(data, user, category=None, group=None):
    cal = Calendar.from_ical(data)
    created_count = 0
    updated_count = 0
    for event in cal.walk('vevent'):
        event_data = {'created_by': user,
                      'title': event.get('summary'),
                      'start_date': event.get('dtstart').dt,
                      'end_date': event.get('dtend').dt,
                      }
        if group:
            event_data['group'] = group
        if category:
            event_data['category'] = category
        event_uuid = str(event.get('uid'))
        try:
            uuid.UUID(event_uuid)
        except ValueError:
            event_uuid, c = UUIDMapping.objects.get_or_create(mapped_string=event_uuid)
            event_uuid = event_uuid.uuid

        e, created = Event.objects.update_or_create(uuid=event_uuid, defaults=event_data)
        if created:
            created_count += 1
        else:
            updated_count += 1
    return created_count, updated_count
