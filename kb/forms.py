from django import forms
from swts.kb.models import *

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category


class ArticleForm(forms.ModelForm):

    class Meta:
        model  = Article 
        fields = ('title', 'keywords', 'contents')
