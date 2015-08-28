from django.db import models
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.db.models import Q

from profiles.models import Profile


class Event(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    location = models.CharField(max_length=100, verbose_name=_('Location'))
    description = models.TextField(verbose_name=_('Description'))
    start_date = models.DateTimeField(verbose_name=_('Start'))
    end_date = models.DateTimeField(verbose_name=_('End'))
    details = models.TextField(verbose_name=_('Details'), null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name=_('Group'))
    created_by = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def send_email_notifications(self):
        users = Profile.objects.filter(email_notifications=True)
        if self.group:
            users = users.filter(user__groups=self.group)
        messages = []
        for u in users:
            if u.user.email != '':
                messages.append((self.title, render_to_string('events/event_notification.txt',
                                                              {'event': self, 'name': u.user.first_name}),
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
        return '{} is attending {}'.format(user, event)

    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)

def get_next_events(request, number_of_events):
    events = Event.objects.filter(Q(start_date__gte=timezone.now())
                                 | Q(start_date__lte=timezone.now()),
                                 Q(end_date__gte=timezone.now())).order_by('start_date')
    if request.user.is_authenticated():
        events = events.filter(Q(group__id__in=request.user.groups.values_list('id', flat=True))
                              | Q(group__isnull=True))
    else:
        events = events.exclude(group__isnull=False)
    return events
