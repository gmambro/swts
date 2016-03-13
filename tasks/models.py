from django.db import models
from django.contrib import auth
from django.db.models import signals

# the tree manager
import mptt 

TASK_STATUS_CHOICES = (
    ('O', 'Opened'    ),
    ('C', 'Closed'    ),
    ('W', 'Working'   ),
    ('S', 'Suspended' )
)    

class Project(models.Model):
    name         = models.CharField(max_length=64, unique=True)
    description  = models.TextField(max_length=200)
    start_date   = models.DateField()
    expire_date  = models.DateField(null=True, blank=True)


    @models.permalink
    def get_absolute_url(self):
        return ('tasks:view_project', [str(self.id)])


class Task(models.Model):
    name         = models.CharField(max_length=64, unique=True)
    project      = models.ForeignKey(Project,
                                     related_name='tasks')
    parent       = models.ForeignKey('self', 
                                     null=True, blank=True, 
                                     related_name='children')
    description  = models.TextField(max_length=200)
    start_date   = models.DateField()
    expire_date  = models.DateField(null=True, blank=True)
    completion   = models.IntegerField(default=0, null=False)
    taskcategory = models.ForeignKey('TaskCategory', null=True, blank=True)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True)
    status       = models.CharField(max_length=1, 
                                    choices=TASK_STATUS_CHOICES,
                                    default='O')   
    owner        = models.ForeignKey(auth.models.User,
                                     related_name='owned_tasks')
    workers      = models.ManyToManyField(auth.models.User, blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('tasks:view_task', [str(self.id)])



mptt.register(Task, order_insertion_by=['name'])


class TaskCategoryManager(models.Manager):
    def toplevels(self):
        qs = super(TaskCategoryManager, self)
        return qs.get_query_set().filter(parent=None)
        

    def toplevels_stats(self):
        from django.db import connection

        stats = dict()

        cursor = connection.cursor()
        cursor.execute("""
            SELECT c1.id, c1.name, count(*)
            FROM tasks_taskcategory c1, tasks_taskcategory c2
            WHERE c2.top_parent_id = c1.id
            GROUP BY 1
            """)
        for row in cursor.fetchall():
            stats[row[0]] = {
                'id'   : row[0],
                'name' : row[1],
                'children_count' : row[2],
                'tasks_count' : 0
                }

        cursor.execute("""
            SELECT c.top_parent_id, count(*)
            FROM tasks_taskcategory c, tasks_task t
            WHERE c.id = t.taskcategory_id
            GROUP BY 1
            """)
        for row in cursor.fetchall():
            stats[row[0]]['tasks_count']=  row[1]

        return stats.values()


# prefix and topparent are cached info to avoid some extra queries
class TaskCategory(models.Model):
    name        = models.CharField(max_length=32)
    prefix      = models.CharField(max_length=256, blank=True)
    description = models.TextField(max_length=200, blank=True)  
    parent      = models.ForeignKey('self',
                                    blank=True, 
                                    null=True,
                                    related_name='child')
    top_parent   = models.ForeignKey('self',
                                     blank=True, 
                                     null=True,
                                     related_name='descendants')

    # set custom manager
    objects = TaskCategoryManager()


    def _get_parents(self):        
        p_list = []
        c = self
        while c.parent and c.parent is not self:
            c = c.parent
            p_list.append(c)

        p_list.reverse()
        return p_list

    def _check_parents(self):
        p_list = self._get_parents()
        return self not in p_list

    def get_separator(self):
        return '::'

    def save(self, force_insert=False, force_update=False):
        p_list = self._get_parents()
        if self in p_list:
            raise Exception("Cycle in \"parent\" relationship")

        if len(p_list):
            names = [ c.name for c in p_list ]
            self.prefix = self.get_separator().join(names)
            self.top_parent = p_list[0]
        else:
            self.top_parent = self

        # Call the "real" save() method.
        super(TaskCategory, self).save(force_insert, force_update)


    def __unicode__(self):
        if self.prefix:
            return self.prefix + self.get_separator() + self.name
        else:
            return self.name

    class Meta:
        verbose_name        = 'task category'
        verbose_name_plural = 'task categories'    
        ordering            = ( 'name', )



class TaskHistoryEntry(models.Model):
    task        = models.ForeignKey(Task, related_name='history_entries')
    user        = models.ForeignKey(auth.models.User)
    date        = models.DateTimeField()
    description = models.TextField(max_length=200, null=True, blank=True)
    status      = models.CharField(max_length=1, choices=TASK_STATUS_CHOICES)
    
    def __unicode__(self):
        return "%s (%s): %s" % (self.date, self.task, self.status)

    class Meta:
        verbose_name        = 'task history entry'
        verbose_name_plural = 'task history entries'   
        ordering            = ( 'date', )
        get_latest_by       = 'date'


class ResourcePointer(models.Model):
    task        = models.ForeignKey(Task, related_name='pointers')
    url         = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, blank=True)       

    def __unicode__(self):
         return self.url

    class Meta:
        ordering            = ( 'url', )

class LogEntry(models.Model):
    task        = models.ForeignKey(Task, related_name='log_entries')
    user        = models.ForeignKey(auth.models.User,
                                    related_name='log_entries')
    logbook     = models.ForeignKey('Logbook', blank=True, null=True, 
                                    related_name='log_entries')
    asset       = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=200)
    minutes     = models.IntegerField(blank=True, null=True)
    date        = models.DateTimeField()
    
    
    def __unicode__(self):
        return "%s: %s on %s" % (self.date, self.user, self.task)
    
    def short_description(self, length=20):
        if len(self.description) > length:
            return "%s..." % (self.description[:length-3],)
        else:
            return self.description

    class Meta:
        verbose_name        = 'log entry'
        verbose_name_plural = 'log entries'
        ordering            = ( 'date' , )
        get_latest_by       = 'date'
        
class Logbook(models.Model):
    name         = models.CharField(max_length=64, unique=True)
    description  = models.TextField(max_length=200)
   
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('tasks:view_logbook', [str(self.id)])

    class Meta:
        ordering = ( 'name', )
            

#----------------------------------------------------------------------#
#                            triggers                                  #
#----------------------------------------------------------------------#

def update_hist_status(sender, instance, **kwargs):
    task = instance.task
    last_hist = task.history_entries.order_by('-date')[0]

    if last_hist.date > instance.date:
        return

    task.status = instance.status
    task.save()

signals.post_save.connect(update_hist_status, sender=TaskHistoryEntry)
