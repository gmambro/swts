from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.views.generic.simple import redirect_to

from swts.common import lazy_reverse

# enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',          
                       # admin                       
                       (r'^admin/', include(admin.site.urls)),

                       # auth
                       url(r'^login/$',  
                           'django.contrib.auth.views.login'),
                       url(r'^logout/$', 
                           'django.contrib.auth.views.logout_then_login',
                           name='auth_logout'),

                       ( r'^$', 
                         redirect_to, { 'url' : lazy_reverse('tasks:index')}
                         ),
                       )


import swts.common.registry
swts.common.registry.autodiscover()
app_patterns = swts.common.registry.patterns()
urlpatterns += patterns('',  *app_patterns)

if settings.DEBUG:
    urlpatterns += patterns('',
                            ( r'^site_media/(?P<path>.*)$', 
                              'django.views.static.serve', 
                              { 'document_root': settings.MEDIA_ROOT }),
                            )
