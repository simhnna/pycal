from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse

from profiles import views

urlpatterns = patterns('',
        url(r'^activate/(?P<activation_id>[a-zA-Z0-9]+)/$', views.activate, name = 'activate'),

        url(r'^sign_in/$', views.sign_in, name = 'sign_in'),
        url(r'^register/$', views.register, name = 'register'),
        #url(r'^sign_out/$', views.sign_out, name = 'sign_out'),
        #url(r'^change_password/$', views.change_password, name='change_password'),
        url(r'^change_email/$', views.change_email, name='change_email'),
        url(r'^edit_account/$', views.edit_account, name='edit_account'),
        )

urlpatterns += patterns('django.contrib.auth.views',
        #url(r'^sign_in/$','login', {'template_name':'profiles/sign_in.html'}, name='sign_in'),
        url(r'^sign_out/$', 'logout', {'next_page': '/'}, name='sign_out'),
        url(r'^change_password/$', 'password_change',
            {'template_name':'profiles/change_password.html',
                'post_change_redirect':'/'
                }, name='change_password'),
        url(r'^reset_password/$', 'password_reset', 
                {'template_name':'profiles/reset_password.html',
                    'post_reset_redirect':'index',
                    'email_template_name':'profiles/reset_password.txt'
                    }, name='reset_password'),
        url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm', {'template_name':'profiles/password_reset_confirm.html','post_reset_redirect':'index'}, name='password_reset_confirm'),
        )

