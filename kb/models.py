from django.db import models

from django.contrib import auth

class Category(models.Model):
    name         = models.CharField(max_length=64, unique=True)
    description  = models.TextField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('kb:view_category', [str(self.id)])

    class Meta:
        verbose_name_plural = 'categories'
        ordering            = [ 'name' ]

class Article(models.Model):
    title        = models.CharField(max_length=64, unique=True)
    category     = models.ForeignKey(Category, related_name='articles')
    keywords     = models.CharField(max_length=200, blank=True)
    author       = models.ForeignKey(auth.models.User)
    contents     = models.TextField()
    lastupdate   = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('kb:view_article', [str(self.id)])

    class Meta:
        ordering            = [ 'title' ]
