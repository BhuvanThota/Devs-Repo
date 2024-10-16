from django.contrib import admin

# Register your models here.
from .models import *


class ProjectAdmin(admin.ModelAdmin):
    list_filter = ['vote_ratio','tags','created']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Review)
admin.site.register(Tag)