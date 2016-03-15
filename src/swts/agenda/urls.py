from django.conf.urls.defaults import patterns, url
from swts.common import lazy_reverse

from django.views.generic.create_update import create_object, update_object, delete_object
from common.views import restricted_detail, autocomplete_lookup

import models
import forms

urlpatterns = patterns('swts.agenda.views',
                       
                       url(r'^$', 'view_month',  name='month'),

                       url(r'^/$', 'agenda_index', name='index'),

                       )


#----------------------------------------------------------------------#
#                           Notes                                      #
#----------------------------------------------------------------------#

note_detail_info = {
    'queryset'      : models.Note.objects.all(),
    'extra_context' : { 'title' :  'Note' }
}

note_edit_info = {
    'login_required' : True,
    'form_class'     : forms.NoteForm,
    'extra_context' : { 'title' :  'Edit Note' }
}

note_delete_info = {
    'login_required' : True,
    'model'          : models.Note,
    'template_name'  : 'agenda/note_confirm_delete.html',
    'post_delete_redirect' : lazy_reverse('agenda:list_notes')
    }

urlpatterns += patterns('swts.agenda.views',
                       
                        url(r'^note/$', 
                            'list_notes',
                            name='list_notes'),
                            
                        url(r'^note/new$', 
                            'new_note',
                            name='new_note'),
                      
                        url(r'^note/(?P<object_id>\d+)/$', 
                            restricted_detail, note_detail_info,
                            name='view_note'),
                        
                        url(r'^note/(?P<object_id>\d+)/edit$',
                            update_object, note_edit_info,
                            name='edit_note'),

                       url(r'^note/(?P<object_id>\d+)/delete$',
                           delete_object, note_delete_info,
                           name='delete_note')
                       
                        )

#----------------------------------------------------------------------#
#                               Todo                                   #
#----------------------------------------------------------------------#

todo_detail_info = {
    'queryset'      : models.Todo.objects.all(),
    'extra_context' : { 'title' :  'Todo' }
}

todo_edit_info = {
    'login_required' : True,
    'form_class'     : forms.TodoForm,
    'extra_context' : { 'title' :  'Edit Todo' }
}


todo_delete_info = {
    'login_required' : True,
    'model'          : models.Note,
    'template_name'  : 'agenda/note_confirm_delete.html',
    'post_delete_redirect' : lazy_reverse('agenda:list_todo')
    }


urlpatterns += patterns('swts.agenda.views',
                        
                        url(r'^todo/$', 
                            'list_todo',
                            name='list_todo'),
                           
                        url(r'^todo/new$', 
                            'new_todo',
                            name='new_todo'),
                      
                        url(r'^todo/(?P<object_id>\d+)/$', 
                            restricted_detail, todo_detail_info,
                            name='view_todo'),
                        
                        url(r'^todo/(?P<object_id>\d+)/edit$',
                            update_object, todo_edit_info,
                            name='edit_todo'),

                       url(r'^todo/(?P<object_id>\d+)/delete$',
                           delete_object, todo_delete_info,
                           name='delete_todo')
                       
                        )
