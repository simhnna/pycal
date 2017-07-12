from django.conf.urls import url

from pycal.views import profiles as profile_views

urlpatterns = [
    url(r'^edit_account/$', profile_views.edit_account, name='edit_account'),
    url(r'^admin/add_profile/$', profile_views.add_profile, name='add_profile'),
    url(r'^admin/list_profiles/$', profile_views.list_profiles, name='list_profiles'),
    ]
