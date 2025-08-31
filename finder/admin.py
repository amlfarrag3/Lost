from django.contrib import admin
from . import models

admin.site.register(models.MissingPerson)
admin.site.register(models.Searcher)
admin.site.register(models.Report)
