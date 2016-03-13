from django.db import models
from django.contrib import auth

class Note(models.Model):
    owner        = models.ForeignKey(auth.models.User,
				 related_name='agenda_notes')
    contents     = models.TextField(max_length=1024)
    public       = models.BooleanField(default=True)
    shared_with  = models.ForeignKey(auth.models.Group,
                                     null=True, blank=True,
                                     related_name='agenda_notes')

    def __unicode__(self):
        return "Node " + str(self.pk) + " - " + str(self.owner)

    @models.permalink
    def get_absolute_url(self):
        return ('agenda:view_note', [str(self.id)])

class Todo(models.Model):
    owner        = models.ForeignKey(auth.models.User,
				 related_name='agenda_todos')
    title        = models.CharField(max_length=128)
    public       = models.BooleanField(default=True)
    shared_with    = models.ForeignKey(auth.models.Group,
                                       null=True, blank=True,
                                       related_name='agenda_todos')
    expire_date  = models.DateField()
    contents     = models.TextField(max_length=1024)

    def __unicode__(self):
        return "Node " + str(self.pk) + " - " + str(self.owner)


    @models.permalink
    def get_absolute_url(self):
        return ('agenda:view_todo', [str(self.id)])

class Memo(models.Model):
    owner          = models.ForeignKey(auth.models.User,
                                       null=True, blank=True,
                                       related_name='agenda_memos')
    shared_with    = models.ForeignKey(auth.models.Group,
                                       related_name='agenda_memos')
    title        = models.CharField(max_length=128)
    start_datetime = models.DateTimeField()
    end_datetime   = models.DateTimeField()
