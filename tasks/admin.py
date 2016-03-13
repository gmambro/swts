from swts.tasks import models
from django.contrib import admin

admin.site.register(models.Project)
admin.site.register(models.Task)
admin.site.register(models.TaskCategory)
admin.site.register(models.TaskHistoryEntry)
admin.site.register(models.LogEntry)
admin.site.register(models.Logbook)
