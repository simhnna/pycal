from django.conf.urls import patterns, url

from django.contrib.auth import views as auth_views
from pycal.views import profiles as profile_views

urlpatterns = [
    url(r'^activate/(?P<activation_id>[a-zA-Z0-9]+)/$', profile_views.activate, name='activate'),
    url(r'^register/$', profile_views.register, name='register'),
    url(r'^edit_account/$', profile_views.edit_account, name='edit_account'),
    url('^login/$', auth_views.login, {'template_name': 'profiles/sign_in.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'profiles/reset_password.html', 'post_reset_redirect': 'index', 'email_template_name': 'profiles/reset_password.txt'}, name='reset_password'),
    url(r'^password_change/$', auth_views.password_change, {'template_name': 'profiles/change_password.html', 'post_change_redirect': '/'}, name='change_password'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'template_name': 'profiles/password_reset_confirm.html', 'post_reset_redirect': 'index'}, name='password_reset_confirm'),
    url(r'^admin/add_profile/$', profile_views.add_profile, name='add_profile'),
    url(r'^admin/list_profiles/$', profile_views.list_profiles, name='list_profiles'),
    ]
