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
from events.funcs import parse_ical


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = _('Categories')
        verbose_name = _('Category')

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    location = models.CharField(max_length=100, verbose_name=_('Location'), null=True, blank=True)
    description = models.TextField(verbose_name=_('Description'))
    dtstart = models.DateTimeField(verbose_name=_('Start'))
    dtend = models.DateTimeField(verbose_name=_('End'), blank=True, null=True)
    all_day = models.BooleanField(verbose_name=_('All day'), default=False)
    details = models.TextField(verbose_name=_('Details'), null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name=_('Group'))
    category = models.ForeignKey(Category, null=True, blank=True)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False)
    recurrence_id = models.DateTimeField(null=True, blank=True)

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


class Recurrence(models.Model):
    event = models.ForeignKey(Event)
    dtstart = models.DateTimeField(verbose_name=_('Start'))
    dtend = models.DateTimeField(verbose_name=_('End'), blank=True, null=True)

    def get_absolute_url(self):
        return reverse('events:recurrence_detail', args=(self.id,))

    @property
    def title(self):
        return self.event.title

    @property
    def location(self):
        return self.event.location

    @property
    def description(self):
        return self.event.description

    @property
    def all_day(self):
        return self.event.all_day

    @property
    def category(self):
        return self.event.category

    @property
    def group(self):
        return self.event.group

    @property
    def created_by(self):
        return self.event.created_by

    @property
    def details(self):
        return self.event.details


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
    created_count = 0
    updated_count = 0
    events = parse_ical(data)
    for event in events:
        event_data = {'created_by': user,
                      'title': event.summary,
                      'dtstart': event.dtstart,
                      'dtend': event.dtend,
                      'location': event.location,
                      'description': event.description,
                      }
        if group:
            event_data['group'] = group
        if category:
            event_data['category'] = category
        if not event.description:
            event_data['description'] = event.summary
        event_uuid = event.uid
        try:
            uuid.UUID(event_uuid)
        except ValueError:
            event_uuid, c = UUIDMapping.objects.get_or_create(mapped_string=event_uuid)
            event_uuid = event_uuid.uuid

        e, created = Event.objects.update_or_create(uuid=event_uuid,
                                                    recurrence_id=event.recurrence_id,
                                                    defaults=event_data)
        if created:
            created_count += 1
        else:
            updated_count += 1
        if event.recurrences:
            for recurrence in Recurrence.objects.filter(event=e):
                if recurrence.dtstart in event.recurrences:
                    event.recurrences.remove(recurrence.dtstart)
                else:
                    recurrence.delete()
            for begining in event.recurrences:
                Recurrence.objects.create(event=e, dtstart=begining, dtend=begining+event.duration)


    return created_count, updated_count
