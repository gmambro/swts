from django import forms
from swts.common.widgets import CalendarWidget

from models import Note, Todo

class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        exclude = ( 'owner' )

class TodoForm(forms.ModelForm):
    expire_date = forms.DateField(widget=CalendarWidget())

    class Meta:
        exclude = ( 'owner' )
        model = Todo
