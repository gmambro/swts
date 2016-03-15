from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.views.generic.create_update import update_object, delete_object

from swts.common import lazy_reverse
from swts.common.views import restricted_detail, restricted_object_list

import models
import forms

incident_list_info = {
    'queryset'      : models.Incident.objects.all(),
    'extra_context' : { 'title' :  'Incidents List' }
}

incident_detail_info = {
    'queryset'      : models.Incident.objects.all(),
    'extra_context' : { 'title' :  'View Incident' }
}

incident_edit_info = {
    'login_required' : True,
    'form_class'     : forms.IncidentForm,
    'extra_context' : { 'title' :  'Edit Incident' }
    }

incident_delete_info = {
    'login_required' : True,
    'model'          : models.Incident,
    'post_delete_redirect' : lazy_reverse('cid:list_incidents')
    }

urlpatterns = patterns('swts.cid.views',
                       
                       url(r'^$', 'index',  name='index'),

                       url(r'^incident/$', 
                           restricted_object_list, incident_list_info,
                           name='list_incidents'),

                       url(r'^incident/new',
                           'new_incident',
                           name = 'new_incident'),

                       url(r'^incident/(?P<object_id>\d+)/$',
                           restricted_detail, incident_detail_info,
                           name='view_incident'),

                       url(r'^incident/(?P<object_id>\d+)/edit$',
                           update_object, incident_edit_info,
                           name='edit_incident'),

                       url(r'^incident/(?P<object_id>\d+)/delete$',
                          delete_object, incident_delete_info,
                           name='delete_incident'),                      
                      
                       )
