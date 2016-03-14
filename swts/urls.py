from django.conf.urls import patterns, url, include
from django.conf import settings

from django.views.generic import RedirectView

from common import lazy_reverse

# enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',          
                       # admin                       
                       (r'^admin/', include(admin.site.urls)),
                       # redirect home
                       ( r'^$',
                         RedirectView.as_view(url=lazy_reverse('tasks:index'))
                         ),
                       url(r'^tasks/', include('tasks.urls', namespace='tasks')),
                       url(r'^cid/', include('cid.urls', namespace='cid')),
                       url(r'^kb/', include('kb.urls', namespace='kb')),                       
                       # auth
                       url(r'^accounts/login/$',  'django.contrib.auth.views.login', 
	                       { 'authentication_form' : LoginForm },
                           name='login' ),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', 
                           name='logout'),
)
