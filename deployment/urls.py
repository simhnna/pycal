from django.conf.urls import include, url
from django.contrib import admin
from django.utils import timezone
import deployment.views

now = timezone.now()

urlpatterns = [
    # Examples:
    # url(r'^$', 'pycal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^profiles/', include('pycal.urls.profiles', namespace='profiles')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^events/', include('pycal.urls.events', namespace='events')),
    url(r'^$', deployment.views.home, name='index'),
    url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)/', deployment.views.calendar_view, name='calendar_specific'),
    url(r'^calendar$', deployment.views.calendar_view, {'month': now.month, 'year': now.year}, name='calendar'),
    url(r'^feedinfo$', deployment.views.feed, name='feedinfo'),
]
