import models
import forms

from common.shortcuts import make_response

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from django.template import RequestContext

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from django.views.generic import list_detail
from django.views.generic.create_update import delete_object

from django.db.models import Count, Q

from datetime import datetime, date

#----------------------------------------------------------------------#
#                             overview                                 #
#----------------------------------------------------------------------#

@login_required
def overview(request):
    task_list = models.Task.objects.filter(status__exact='O').order_by('expire_date')
    task_searchform = forms.TaskSearchForm(callback=reverse('tasks:task_lookup'))

    params = { 
        'title'         : 'Overview',
        'task_list'     : task_list,
        'task_searchform' : task_searchform,
        }
    return make_response('tasks/overview.html', request, params)

@login_required
def stats(request):

    total_tasks = models.Task.objects.count()

    # task by status stats
    status_stats = []
    count_by_status = {}
    task_count = models.Task.objects.values('status').annotate(Count('status'))
    for t in task_count:
        count_by_status[t['status']] = t['status__count']
    for c in TASK_STATUS_CHOICES:
        status_stats.append({
            'status'          : c[0],
            'status_display'  : c[1],
            'count'           : count_by_status.get(c[0], 0)
            })

    # task by top categories
    category_stats = models.TaskCategory.objects.toplevels_stats()

    params = { 
        'status_stats'  : status_stats,
        'total_tasks'   : total_tasks,
        'category_stats': category_stats,
        'title'         : 'Stats',
        }

    return make_response('tasks/stats.html', request, params)

#----------------------------------------------------------------------#
#                             projects                                 #
#----------------------------------------------------------------------#

@login_required
def new_project(request):
    if request.method == 'POST':
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return HttpResponseRedirect(reverse('tasks:view_project', 
                                                kwargs={'object_id': project.pk }) 
                                        )
    else:
        initial_dict = {
            'start_date'     : date.today()            
            }
        form = forms.ProjectForm(initial=initial_dict)

    params = {
        'title' : 'New Project',
        'form'  : form 
        }
    return make_response('tasks/project_form.html', request, params)

@login_required
def view_project(request, object_id):
    obj = get_object_or_404(models.Project, pk=object_id)

    tree_mgr = models.Task._tree_manager
    tasks = obj.tasks.order_by(tree_mgr.tree_id_attr, tree_mgr.left_attr)
    params = {
            'title'      : 'Project ' + obj.name,
            'object'     : obj,
            'tasks'      : tasks,
            }    

    return make_response('tasks/project_detail.html', 
                         request, params)

@login_required
def view_project_jsgantt_xml(request, object_id):
    project = get_object_or_404(models.Project, pk=object_id)

    tree_mgr = models.Task._tree_manager
    tasks = project.tasks.order_by(tree_mgr.tree_id_attr, tree_mgr.left_attr)

    params = {
            'project'    : project,
            'tasks'      : tasks
            }    
    response = HttpResponse(mimetype="text/xml")
    t = loader.get_template("tasks/project_jsgantt.xml")
    c = Context(params)
    response.write(t.render(c))
    return response


@login_required
def list_projects(request, status=None):
    message = ''

    objects = models.Project.objects
    if status:
        qs = objects.filter(status__exact=status)
    else:
        if request.method and 'name' in request.POST:
            name = request.POST['name']
            qs = objects.filter(name__icontains = name)
            message = 'Search results for %s' % name
        else:
            qs = objects.all()

    extra = {
        'title'   : 'Project List',
        'message' : message
        }

    return list_detail.object_list(request,
                                   queryset = qs.order_by('-start_date'),
                                   extra_context = extra)



#----------------------------------------------------------------------#
#                                tasks                                 #
#----------------------------------------------------------------------#


@login_required
def list_tasks(request, status=None, category_id=None):
    message = ''

    objects = models.Task.objects
    if status:
        qs = objects.filter(status__exact=status)
    elif category_id:
        category = get_object_or_404(TaskCategory, pk=category_id)
        title = 'Tasks in category ' + category.name
        qs = objects.filter(Q(taskcategory=category_id) | 
                            Q(taskcategory__top_parent=category_id))
    else:
        if request.method and 'name' in request.POST:
            name = request.POST['name']
            qs = objects.filter(name__icontains = name)
            message = 'Search results for %s' % name
        else:
            qs = objects.all()

    searchform = forms.TaskSearchForm(callback=reverse('tasks:task_lookup'))

    extra = {
        'title'   : 'Task List',
        'message' : message,
        'searchform'    : searchform,
        }

    return list_detail.object_list(request,
                                   queryset = qs.order_by('-start_date'),
                                   extra_context = extra)


@login_required
def view_task(request, object_id):
    obj = get_object_or_404(models.Task, pk=object_id)

    try:
        last_histentry = obj.history_entries.latest()
    except:
        last_histentry = None
    
    try:
        last_logentry = obj.log_entries.latest()
    except:
        last_logentry = None

    logbooks = models.Logbook.objects.select_related().filter(log_entries__task = object_id)

    params = { 
        'title'          : 'Task ' + obj.name,
        'object'         : obj,
        'last_histentry' : last_histentry,
        'last_logentry'  : last_logentry,
        'logbooks'       : logbooks,        
        }

    return make_response('tasks/task_detail.html', request, params)


@login_required
def new_task(request, project_id=None, task_id=None):
    if not project_id and not task_id:
        raise TypeError("a project_id or a task_id is needed")

    parent = None
    if task_id:
        parent = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner   = request.user
            if project_id:
                task.project_id = project_id
            else:
                task.project = Task.objects.get(pk=task_id).project

            task.save()
            form.save_m2m()
            if parent:
                task.move_to(parent)

            return HttpResponseRedirect(reverse('tasks:view_task', 
                                                kwargs={'object_id': task.pk }) 
                                        )
    else:
        initial_dict = {
            'start_date'     : date.today()            
            }
        form = forms.TaskForm(initial=initial_dict)

    params = {
        'title' : 'New Task',
        'form'  : form 
        }
    return make_response('tasks/task_form.html', request, params)



#----------------------------------------------------------------------#
#                                 logentry                             #
#----------------------------------------------------------------------#

@login_required
def user_view(request):
    user = request.user

    my_tasks = user.owned_tasks()
    other_tasks = user.task_set.exclude(owner=user)

    last_logentries = user.logentry_set.order_by('-date')[:5]



@login_required
def add_logentry(request, task_id):
    if request.method == 'POST':
        form = forms.LogEntryForm(request.POST)
        if form.is_valid():
            logentry = form.save(commit=False)
            logentry.task_id = task_id
            logentry.user    = request.user
            logentry.save()
            return HttpResponseRedirect(reverse('tasks:view_task', 
                                                kwargs={'object_id': task_id}) 
                                        )
    else:
        initial_dict = {
            'task_id'  : task_id,
            'date'     : datetime.now()
            }
        form = forms.LogEntryForm(initial=initial_dict)

    return make_response('tasks/add_logentry.html', request,
                         { 'form': form })


@login_required
def list_logentry(request, task_id):
    task = models.Task.objects.get(id = task_id)
    extra_context =  { 
        'title' :  'Task log entries',
        'task'  : task
        }
    return list_detail.object_list(request,
                                   queryset = task.log_entries.all(),
                                   extra_context = extra_context
                                   ) 


#----------------------------------------------------------------------#
#                                 history                              #
#----------------------------------------------------------------------#


@login_required
def add_history(request, task_id):
    if request.method == 'POST':
        form = forms.HistoryForm(request.POST)
        if form.is_valid():
            h = form.save(commit=False)
            h.task_id = task_id
            h.user_id = request.user.pk
            h.save()
            return HttpResponseRedirect(reverse('tasks:view_task', 
                                                kwargs={'object_id': task_id}) 
                                        )
    else:
        initial_dict = {
            'task_id'  : task_id,
            'date'     : datetime.now()
            }
        form = forms.HistoryForm(initial=initial_dict)

    return make_response('tasks/add_history.html', request, { 'form': form })


@login_required
def list_history(request, task_id):
    task = models.Task.objects.get(id = task_id)
    extra_context =  { 
        'title'   : 'Task history',
        'task'    : task,
        }
    return list_detail.object_list(request,
                                   queryset = task.history_entries.all(),
                                   template_name = 'tasks/taskhistory_list.html',
                                   extra_context = extra_context
                                   )

#----------------------------------------------------------------------#
#                              logbooks                                #
#----------------------------------------------------------------------#

@login_required
def list_logbooks(request):
    return list_detail.object_list(request,
                                   queryset = models.Logbook.objects.all(),
                                   template_name = 'tasks/logbook_list.html',
                                   extra_context = { 'title' :  'Logbooks' })


#----------------------------------------------------------------------#
#                            resource pointers                         #
#----------------------------------------------------------------------#


@login_required
def list_pointers(request):
    #  TODO prefetch on pointer
    qs = models.Task.objects.select_related('pointers').annotate(n_pointers=Count('pointers')).filter(n_pointers__gt=1)

    return list_detail.object_list(request,
                                   queryset = qs,
                                   template_name = 'tasks/pointer_list.html',
                                   extra_context = { 'title' :  'Resource Pointers' })


@login_required
def add_pointer(request, task_id):
    if request.method == 'POST':
        form = forms.ResourcePointerForm(request.POST)
        if form.is_valid():
            logentry = form.save(commit=False)
            logentry.task_id = task_id
            logentry.save()
            return HttpResponseRedirect(reverse('tasks:view_task', 
                                                kwargs={'object_id': task_id}) 
                                        )
    else:
        initial_dict = {
            'task_id'  : task_id,
            }
        form = forms.ResourcePointerForm(initial=initial_dict)

    return make_response('tasks/pointer_form.html', request,
                         { 'form': form })


@login_required
def delete_pointer(request, object_id):
    p = ResourcePointer.objects.get(pk=object_id)
    info = {
        'login_required' : False,
        'model'          : ResourcePointer,
        'object_id'      : object_id,
        'template_name'  : 'tasks/pointer_confirm_delete.html',
        'post_delete_redirect' : reverse('tasks:view_task',
                                         kwargs={'object_id':p.task.pk})
        }
    return delete_object(request, **info)
