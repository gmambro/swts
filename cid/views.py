import models
import forms

from django.contrib.auth.decorators import login_required

from swts.common.shortcuts import make_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


def index(request):
    return HttpResponse("TODO")

@login_required
def new_incident(request):
    if request.method == 'POST':
        form = forms.IncidentForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.owner = request.user
            object.save()
            return HttpResponseRedirect(reverse('agenda:view_note', 
                                                kwargs={'object_id': object.id}) 
                                        )
    else:
        form = forms.IncidentForm()

    return make_response('cid/incident_form.html', request,
                         { 'form': form })

