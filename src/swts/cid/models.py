from django.db import models
from django.contrib import auth

YN_EXT_CHOICES = (
    ('Y', 'Yes'           ),
    ('N', 'No'            ),
    ('U', 'Unknown'       ),
    ('A', 'Not Appliable' )
)    

class IncidentDetectionMode(models.Model):
    name         = models.CharField(max_length = 64, unique=True)

    def __unicode__(self):
        return self.name

class IncidentAttachment(models.Model):
    incident      = models.ForeignKey('Incident',
                                    related_name='attachments')
    attached_file = models.FileField(upload_to='attachments')
    mimetype      = models.CharField(max_length=64, editable=False)
    created       = models.DateTimeField(auto_now_add=True, editable=False)   

class Incident(models.Model):
    reporter     =  models.ForeignKey(auth.models.User,
                                     related_name='reported_incidents')
    
    creation_ts  = models.DateTimeField(auto_now_add=True, editable=False)

    start_dt        = models.DateTimeField(
                            verbose_name="Approx time the incident started"
                        )
    detection_dt    = models.DateTimeField(
                        verbose_name="Time the incident was detected"
                        )     
    detection_mode  = models.ForeignKey(IncidentDetectionMode)    
    
    impacted_systems = models.IntegerField(
                          null = True,
                          verbose_name="Number of impacted systems"
                          )
    data_loss            = models.CharField(max_length = 1, 
                                            choices = YN_EXT_CHOICES,
                                            default = 'A')
    service_interruption = models.CharField(max_length = 1, 
                                            choices = YN_EXT_CHOICES,
                                            default = 'A')

    description  = models.TextField(max_length=200)
    log_snippet  = models.TextField(max_length=200, blank = True, null = True)

    def __unicode__(self):
        return u"Incident ID %d" % (self.id)

    def short_description(self, length=20):
        if len(self.description) > length:
            return "%s..." % (self.description[:length-3],)
        else:
            return self.description
    
    @models.permalink
    def get_absolute_url(self):
        return ('cid:view_incident', [str(self.id)])

    class Meta:
        ordering            = ( 'creation_ts', )
