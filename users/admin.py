from django.contrib import admin

# Register your models here.
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['username', 'name',]

class SkillAdmin(admin.ModelAdmin):
    list_filter = ['name',]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill, SkillAdmin)