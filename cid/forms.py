from django import forms
from swts.common.widgets import CalTimeWidget

import models

class IncidentForm(forms.ModelForm):
    start_dt = forms.SplitDateTimeField(widget=CalTimeWidget())
    detection_dt = forms.SplitDateTimeField(widget=CalTimeWidget())

    class Meta:
        model   = models.Incident
        exclude = ( 'reporter' )
