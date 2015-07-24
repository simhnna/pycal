from django.conf.urls import patterns, url

from events import views
from events.feeds import EventFeed

urlpatterns = patterns('',
        url(r'^new/$', views.create_event, name = 'create_event'),
        url(r'^(?P<event_id>\d+)/edit$', views.edit_event, name='edit_event'),
        url(r'^(?P<event_id>\d+)/delete$', views.delete_event, name='delete_event'),
        url(r'^(?P<event_id>\d+)$', views.detail, name='detail'),
        url(r'^public_feed.ics$', EventFeed(), name='feed'),
        )
