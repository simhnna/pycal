from django.conf.urls import url

from pycal.views import events as event_views
from pycal.feeds import EventFeed

urlpatterns = [
    url(r'^new/$', event_views.create_event, name='create_event'),
    url(r'^(?P<event_id>\d+)/edit$', event_views.edit_event, name='edit_event'),
    url(r'^(?P<event_id>\d+)/delete$', event_views.delete_event, name='delete_event'),
    url(r'^(?P<event_id>\d+)$', event_views.detail, name='detail'),
    url(r'^public_feed/feed.ics$', EventFeed()),
    url(r'^private_feed/(?P<feed_id>[a-zA-Z0-9]+)/feed.ics$', EventFeed()),
    url(r'^public_feed/feed.ical$', EventFeed(), name='public_feed'),
    url(r'^public_feed.ics$', EventFeed()),
    url(r'^upload_ical$', event_views.upload_ical, name='upload_ical'),
    url(r'^private_feed/(?P<feed_id>[a-zA-Z0-9]+)/feed.ical$', EventFeed(), name='private_feed'),
    url(r'^(?P<event_id>\d+)/attend$', event_views.attend, name='attend'),
    url(r'^(?P<event_id>\d+)/unattend$', event_views.unattend, name='unattend'),
    ]
