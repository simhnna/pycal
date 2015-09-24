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
        if feed_id:
            user = Profile.objects.get(feed_id=feed_id).user
            return Event.objects.filter(Q(group__isnull=True)|Q(group__id__in=user.groups.values_list('id',
                flat=True))).order_by('-start_date')
        else:
            return Event.objects.filter(group__isnull=True).order_by('-start_date')

    def items(self, obj):
        return obj

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        if item.all_day:
            return item.start_date.date() + datetime.timedelta(days=1)
        else:
            return item.start_date

    def item_end_datetime(self, item):
        if item.all_day:
            return item.start_date.date() + datetime.timedelta(days=2)
        else:
            return item.end_date

    def item_location(self, item):
        return item.location
