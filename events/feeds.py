from django_ical.views import ICalFeed
from events.models import Event
from profiles.models import Profile
from django.db.models import Q

import datetime

class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = '-//pycal.serve-me.info//Events//DE'
    timezone = 'UTC'
    file_name = "events.ical"
    private = False

    def get_object(self, request, feed_id=None):
        to_return = []
        if feed_id:
            user = Profile.objects.get(feed_id=feed_id).user
            to_return += list(Event.objects.filter(Q(group__isnull=True)|Q(group__id__in=user.groups.values_list('id',
                flat=True))).order_by('-dtstart'))
        else:
            to_return += list(Event.objects.filter(group__isnull=True).order_by('-dtstart'))
        return to_return

    def items(self, obj):
        return obj

    def item_title(self, item):
        if hasattr(item, 'event'):
            return item.event.title
        else:
            return item.title

    def item_description(self, item):
        if hasattr(item, 'event'):
            return item.event.description
        else:
            return item.description

    def item_start_datetime(self, item):
        if hasattr(item, 'event'):
            return item.dtstart
        else:
            if item.all_day:
                return item.dtstart.date() + datetime.timedelta(days=1)
            else:
                return item.dtstart

    def item_end_datetime(self, item):
        if hasattr(item, 'event'):
            return item.dtend
        else:
            if item.all_day:
                return item.dtstart.date() + datetime.timedelta(days=2)
            else:
                return item.dtend

    def item_location(self, item):
        if hasattr(item, 'event'):
            return item.event.location
        else:
            return item.location
