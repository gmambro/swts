from swts.kb.models import *
import forms

from django.contrib.auth.decorators import login_required
from django.views.generic import list_detail,create_update
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.template import RequestContext

@login_required
def delete_article(request, object_id):
    a = Article.objects.get(pk=object_id)
    info = {
        'object_id'      : object_id,
        'model'          : Article,
        'login_required' : False,
        'post_delete_redirect' : reverse('kb:view_category',
                                         kwargs={'object_id':a.category.pk})
        }
    return create_update.delete_object(request, **info)


# used for both articles and categories
@login_required
def detail(*args, **kwargs):
    return list_detail.object_detail(*args, **kwargs)


@login_required
def list_categories(request):
    qs = Category.objects.all().order_by('name')
    return list_detail.object_list(request,
                                   queryset = qs,
                                   extra_context = { 'title':  'Articles' })

@login_required
def add_article(request, category_id):
    if request.method == 'POST':
        form = forms.ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.category_id = category_id
            article.author_id = request.user.pk
            article.save()
            return HttpResponseRedirect(
                reverse('kb:view_article',
                        kwargs={'object_id': article.pk}) 
                )
    else:
        initial_dict = {
            'category_id'  : category_id,
            }
        form = forms.ArticleForm(initial=initial_dict)

    params = {
        'title' : 'New article',
        'category' : Category.objects.get(pk=category_id),
        'form'  : form
        }
    return render_to_response('kb/article_form.html', 
                              params,
                              context_instance=RequestContext(request))
                              
