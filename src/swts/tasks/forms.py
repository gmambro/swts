from django import forms

import models
from swts.common.widgets import \
    CalendarWidget, CalTimeWidget, \
    AutoCompleteText
#import mptt.forms

from datetime import date, datetime


class ProjectForm(forms.ModelForm):
    start_date  = forms.DateField(widget=CalendarWidget())
    expire_date = forms.DateField(widget=CalendarWidget(),
                                  required=False)

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args,**kwargs) # populates the post
        if not self.instance:
            return

    class Meta:
        exclude = ( 'owner', 'pointers' )
        model   = models.Project

class TaskForm(forms.ModelForm):
    start_date  = forms.DateField(widget=CalendarWidget())
    expire_date = forms.DateField(widget=CalendarWidget(),
                                  required=False)
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args,**kwargs) # populates the post
        if not self.instance:
            return

    class Meta:
        exclude = ( 'owner', 'project', 'parent', 'pointers' )
        model   = models.Task


class TaskSearchForm(forms.Form):
    name    = forms.CharField()

    def __init__(self, *args, **kwargs):
        callback = kwargs.pop('callback', None)
        if callback is None:
            raise TypeError("Missing callback parameter value")

        super(TaskSearchForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget=AutoCompleteText(callback=callback)


class LogEntryForm(forms.ModelForm):
    date    = forms.SplitDateTimeField(widget=CalTimeWidget())

    def clean_date(self):
        cleaned_date = self.cleaned_data['date']
        if cleaned_date > datetime.now():
            raise forms.ValidationError("Date is in the future")
        return cleaned_date

    class Meta:
        fields = ( 'date', 'logbook', 'asset', 'description', 'minutes' )
        model  = models.LogEntry

class HistoryForm(forms.ModelForm):
    date    = forms.SplitDateTimeField(widget=CalTimeWidget())

    def clean_date(self):
        cleaned_date = self.cleaned_data['date']
        if cleaned_date > datetime.now():
            raise forms.ValidationError("Date is in the future")
        return cleaned_date

    class Meta:       
        fields = ( 'date', 'status', 'description')
        model  = models.TaskHistoryEntry

class ResourcePointerForm(forms.ModelForm):
    
    class Meta:
        fields = ( 'url', 'description' )
        model = models.ResourcePointer
