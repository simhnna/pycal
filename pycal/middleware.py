from django.utils import timezone

import pytz


class TimezoneMiddleware(object):
    @staticmethod
    def process_request(request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
