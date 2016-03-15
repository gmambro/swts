from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object, update_object

import views, models, forms
from common.views import restricted_detail, autocomplete_lookup

urlpatterns = []

#----------------------------------------------------------------------#
#                           Project                                    #
#----------------------------------------------------------------------#

project_edit_info = {
    'login_required' : True,
    'form_class'     : forms.ProjectForm,
    'extra_context' : { 'title' :  'Edit Project' }
}

urlpatterns += patterns('swts.tasks.views',
                        
                        url(r'^project/$', 
                            'list_projects',
                            name='list_projects'),
                            
                        url(r'^project/new$', 
                            'new_project',
                            name='new_project'),
                      
                        url(r'^project/(?P<object_id>\d+)/$', 
                            'view_project',
                            name='view_project'),

                        url(r'^project/(?P<object_id>\d+)/jsgantt.xml$', 
                            'view_project_jsgantt_xml',
                            name='view_project_jsgantt_xml'),
                        
                        url(r'^project/(?P<object_id>\d+)/edit$',
                            update_object, project_edit_info,
                            name='edit_project')
                        )


#----------------------------------------------------------------------#
#                           Task                                       #
#----------------------------------------------------------------------#

task_edit_info = {
    'login_required' : True,
    'form_class'     : forms.TaskForm,
    'extra_context' : { 'title' :  'Edit Task' }
}


# ajax callback
task_lookup_info = {
	'queryset' :  models.Task.objects.all(),
	'field'    : 'name',
	'limit'    : 10,
	'login_required': True, 
}

urlpatterns += patterns('swts.tasks.views',

                        url(r'^project/(?P<project_id>\d+)/add_task$', 
                            'new_task',
                            name='add_task'),
                        
                        url(r'^task/$', 
                            'list_tasks',
                            name='list_tasks'),
    
                        url(r'^task/status/(?P<status>\w)/$', 
                            'list_tasks',
                            name='list_task_status'),
                        
                        url(r'^task/category/(?P<category_id>\d+)/$', 
                            'list_tasks',
                            name='list_task_category'),
                        
                        url(r'^task/(?P<task_id>\d+)/add_subtask$', 
                            'new_task',
                            name='add_subtask'),
                      
                        url(r'^task/(?P<object_id>\d+)/$', 
                            'view_task',
                            name='view_task'),
                        
                        url(r'^task/(?P<object_id>\d+)/edit$',
                            update_object, task_edit_info,
                            name='edit_task'),

                        # ajax support functions
                        url(r'^task/lookup$', 
                            autocomplete_lookup, task_lookup_info,
                            name = 'task_lookup'),
                        
                        # history
                        url(r'^task/(?P<task_id>\d+)/add_history$', 
                            'add_history',
                            name='add_history'),
                        
                        url(r'^task/(?P<task_id>\d+)/history/', 
                            'list_history',
                            name='list_history'),
                                                
                       )

#----------------------------------------------------------------------#
#                        Category                                      #
#----------------------------------------------------------------------#

# urlpatterns += patterns('swts.tasks.views',                       
#                       url(r'^category/(?P<object_id>\d+)/$', 
#                           'view_category',
#                           name='view_category'),
#                        )

#----------------------------------------------------------------------#
#                         Pointer                                      #
#----------------------------------------------------------------------#


pointer_edit_info = {
    'login_required' : True,
    'form_class'     : forms.ResourcePointerForm,
    'template_name'  : 'tasks/pointer_form.html',
    'extra_context'  : { 'title' :  'Edit pointer' },    
}

urlpatterns += patterns('swts.tasks.views',

                       url(r'^pointer/$',
                           'list_pointers',
                           name='list_pointers'),

                       url(r'^task/(?P<task_id>\d+)/add_pointer$', 
                           'add_pointer',
                           name='add_pointer'),

                       url(r'^pointer/(?P<object_id>\d+)/edit$',
                           update_object, pointer_edit_info,
                           name='edit_pointer'),

                       url(r'^pointer/(?P<object_id>\d+)/delete$',
                           'delete_pointer',
                           name='delete_pointer'),

                        )

#----------------------------------------------------------------------#
#                         Logbook                                      #
#----------------------------------------------------------------------#


logbook_detail_info = {
    'queryset'      : models.Logbook.objects.all(),
    'extra_context' : { 'title' :  'Logbook' }
    }

urlpatterns += patterns('swts.tasks.views',

                        url(r'^(?P<task_id>\d+)/add_logentry$', 
                            'add_logentry',
                            name='add_logentry'),

                        url(r'^(?P<task_id>\d+)/logentry/', 
                            'list_logentry',
                            name='list_logentry'),
                      
                        url(r'^logbook/$', 
                            'list_logbooks',
                            name='list_logbooks'),
                        
                        url(r'^logbook/(?P<object_id>\d+)/$', 
                            restricted_detail, logbook_detail_info,
                            name='view_logbook'),
			)
                        
#----------------------------------------------------------------------#
#                      Generic views                                   #
#----------------------------------------------------------------------#


urlpatterns += patterns('swts.tasks.views',

                       url(r'^overview/',
                           'overview',
                           name='overview'),
                       
                       url(r'^$', 'list_tasks',
			       name='index')
                                              
                       )
