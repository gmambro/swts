from django.contrib.auth.decorators import login_required
from django.views.generic import list_detail
from django.utils import simplejson
from django.http import HttpResponse

def autocomplete_lookup(request, queryset, field, limit=5, login_required=False):
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    if request.method == 'POST':
        query = request.POST.get('term', None)
    else:
        query = request.GET.get('term', None)
    if query is None:
        return HttpResponse("")

    obj_list = []
    lookup = { '%s__icontains' % field: query }

    for obj in queryset.filter(**lookup)[:limit]:
        obj_list.append(getattr(obj, field))

    json = simplejson.dumps(obj_list)
    return HttpResponse(json, mimetype = 'application/json')

@login_required
def restricted_detail(*args, **kwargs):
    """Same as the generic object_details but requires login"""
    return list_detail.object_detail(*args, **kwargs)

@login_required
def restricted_object_list(*args, **kwargs):
    """Same as the generic object_list but requires login"""
    return list_detail.object_list(*args, **kwargs)
