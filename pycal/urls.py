from django.conf.urls import include, url
from django.contrib import admin
from django.utils import timezone

now = timezone.now()

urlpatterns = [
    # Examples:
    # url(r'^$', 'pycal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^$', 'pycal.views.home', name='index'),
    url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)/', 'pycal.views.calendar', name='calendar_specific'),
    url(r'^calendar$', 'pycal.views.calendar', {'month': now.month, 'year': now.year}, name='calendar'),
    url(r'^timezone$', 'pycal.views.set_timezone', {}, name='set_timezone'),
]
