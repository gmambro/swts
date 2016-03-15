from django.conf.urls.defaults import *
from django.views.generic.create_update \
    import create_object, update_object, delete_object
from django.core.urlresolvers import reverse

from swts.kb import views, models, forms

category_edit_info = {
    'login_required' : True,
    'form_class'     : forms.CategoryForm,
    'extra_context'  : { 'title' :  'Edit category' }
}

category_detail_info = {
    'queryset'      : models.Category.objects.all(),
    'extra_context' : { 'title' :  'Category' }
}



article_new_info = {
    'login_required' : True,
    'form_class'     : forms.ArticleForm,
    'extra_context'  : { 'title' :  'New article' }
}

article_edit_info = {
    'login_required' : True,
    'form_class'     : forms.ArticleForm,
    'extra_context'  : { 'title' :  'Edit article' }
}


article_detail_info = {
    'queryset'      : models.Article.objects.all(),
    'extra_context' : { 'title' : 'Article' }
}

urlpatterns = patterns('swts.kb.views',                   
                       url(r'^/$', 
                           'list_categories', 
                           name='list_categories'),                           

                       url(r'^/category/(?P<object_id>\d+)/$', 
                           'detail', category_detail_info,
                           name='view_category'),

                       url(r'^/category/(?P<object_id>\d+)/edit$', 
                           update_object, category_edit_info,
                           name='edit_category'),    

                       url(r'^/category/(?P<category_id>\d+)/add_article$', 
                           'add_article',
                           name='add_article'),    
                       
                       url(r'^/article/(?P<object_id>\d+)/$', 
                           'detail', article_detail_info,
                           name='view_article'),      
          
                       url(r'^/article/(?P<object_id>\d+)/edit$', 
                           update_object, article_edit_info,
                           name='edit_article'),  
  
                      url(r'^/article/(?P<object_id>\d+)/delete$', 
                           'delete_article',
                           name='delete_article'),  
                       )
                       
