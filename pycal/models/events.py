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

from pycal.models.profiles import Profile
from pycal.utils.events import parse_ical


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = _('Categories')
        verbose_name = _('Category')

    def __str__(self):
        return self.name


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
        return process_ical_events(data, self)


class Event(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    location = models.CharField(max_length=100, verbose_name=_('Location'), null=True, blank=True)
    description = models.TextField(verbose_name=_('Description'))
    dtstart = models.DateTimeField(verbose_name=_('Start'), blank=True, null=True)
    dtend = models.DateTimeField(verbose_name=_('End'), blank=True, null=True)
    all_day = models.BooleanField(verbose_name=_('All day'), default=False)
    details = models.TextField(verbose_name=_('Details'), null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name=_('Group'))
    category = models.ForeignKey(Category, null=True, blank=True)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False)
    remote_calendar = models.ForeignKey(RemoteCalendar, null=True, blank=True)

    class Meta:
        verbose_name_plural = _('Events')
        verbose_name = _('Event')

    def __str__(self):
        return self.title

    @property
    def duration(self):
        if self.dtend:
            return self.dtend - self.dtstart
        else:
            return None

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
        return reverse('detail', args=(self.id,))

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
    events = Event.objects.filter(Q(dtstart__gte=now) | Q(dtstart__lte=timezone.now(), dtend__gte=timezone.now())).order_by('dtend')
    if request.user.is_authenticated():
        events = events.filter(Q(group__id__in=request.user.groups.values_list('id', flat=True))
                              | Q(group__isnull=True))
    else:
        events = events.exclude(group__isnull=False)
    return events[:number_of_events]


class UUIDMapping(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mapped_string = models.CharField(max_length=120, unique=True, db_index=True)


def process_ical_events(data, remote_calendar):
    category = remote_calendar.category
    user = remote_calendar.user
    group = None
    created_count = 0
    updated_count = 0
    events = parse_ical(data)
    Event.objects.filter(remote_calendar=remote_calendar).delete()
    for event in events:
        event_data = {'created_by': user,
                      'title': event.summary,
                      'dtstart': event.dtstart,
                      'dtend': event.dtend,
                      'location': event.location,
                      'description': event.description,
                      'all_day': event.all_day
                      }
        if group:
            event_data['group'] = group
        if category:
            event_data['category'] = category
        if not event.description:
            event_data['description'] = event.summary
            event.description = event.summary
        event_uuid = event.uid
        try:
            uuid.UUID(event_uuid)
        except ValueError:
            event_uuid, c = UUIDMapping.objects.get_or_create(mapped_string=event_uuid)
            event_uuid = event_uuid.uuid

        e, created = Event.objects.update_or_create(uuid=event_uuid,
                remote_calendar=remote_calendar, defaults=event_data)
        if created:
            created_count += 1
        else:
            updated_count += 1
        for begining in event.recurrences:
            Event.objects.create(created_by=user, title=event.summary,
                    dtstart=begining, dtend=begining+event.duration,
                    location=event.location, description=event.description,
                    group=group, category=category, all_day=event.all_day,
                    remote_calendar=remote_calendar)
    return created_count, updated_count
