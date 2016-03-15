import models
import forms

from common.shortcuts import make_response

from django.db.models import Count, Q
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


#----------------------------------------------------------------------#
#                             overview                                 #
#----------------------------------------------------------------------#


# TODO
def agenda_index(request):
    return HttpResponseRedirect(reverse('agenda:list_notes'))


# TODO
def view_month(request):
    return HttpResponseRedirect(reverse('agenda:list_notes'))


#----------------------------------------------------------------------#
#                               notes                                  #
#----------------------------------------------------------------------#


@login_required
def new_note(request):
    if request.method == 'POST':
        form = forms.NoteForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.owner = request.user
            object.save()
            return HttpResponseRedirect(reverse('agenda:view_note', 
                                                kwargs={'object_id': object.id}) 
                                        )
    else:
        form = forms.NoteForm()

    return make_response('agenda/note_form.html', request,
                         { 'form': form })

@login_required
def list_notes(request):
    extra_context =  { 
        'title'   : 'Notes list',
        }

    user = request.user
    note_filter = (
        Q(owner=request.user) |
        Q(shared_with__user = user))

    qs = models.Note.objects.filter(note_filter)
    return list_detail.object_list(request,
                                   queryset = qs,
                                   extra_context = extra_context
                                   )


#----------------------------------------------------------------------#
#                               todos                                  #
#----------------------------------------------------------------------#

@login_required
def new_todo(request):
    if request.method == 'POST':
        form = forms.TodoForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.owner = request.user
            object.save()
            return HttpResponseRedirect(reverse('agenda:view_todo', 
                                                kwargs={'object_id': object.id}) 
                                        )
    else:
        form = forms.TodoForm()

    return make_response('agenda/todo_form.html', request,
                         { 'form': form })


@login_required
def list_todo(request):
    extra_context =  { 
        'title'   : 'Todo list',
        }
    return list_detail.object_list(request,
                                   queryset = models.Todo.objects.all(),
                                   extra_context = extra_context
                                   )
