from django_ical.views import ICalFeed
from events.models import Event

class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'
    file_name = "events.ics"

    def items(self):
        return Event.objects.filter(group__isnull=True).order_by('-start_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return item.start_date

    def item_end_datetime(self, item):
        return item.end_date

    def item_location(self, item):
        return item.location
