from django.conf.urls import url

from events import views
from events.feeds import EventFeed

urlpatterns = [
   url(r'^new/$', views.create_event, name='create_event'),
   url(r'^(?P<event_id>\d+)/edit$', views.edit_event, name='edit_event'),
   url(r'^(?P<event_id>\d+)/delete$', views.delete_event, name='delete_event'),
   url(r'^(?P<event_id>\d+)$', views.detail, name='detail'),
   url(r'^recurrence/(?P<recurrence_id>\d+)$', views.recurrence_detail, name='recurrence_detail'),
   url(r'^public_feed/feed.ics$', EventFeed()),
   url(r'^private_feed/(?P<feed_id>[a-zA-Z0-9]+)/feed.ics$', EventFeed()),
   url(r'^public_feed/feed.ical$', EventFeed(), name='public_feed'),
   url(r'^public_feed.ics$', EventFeed()),
   url(r'^upload_ical$', views.upload_ical, name='upload_ical'),
   url(r'^private_feed/(?P<feed_id>[a-zA-Z0-9]+)/feed.ical$', EventFeed(), name='private_feed'),
   url(r'^(?P<event_id>\d+)/attend$', views.attend, name='attend'),
   url(r'^(?P<event_id>\d+)/unattend$', views.unattend, name='unattend'),
   ]
