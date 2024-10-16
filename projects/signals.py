from .models import *

# Create your models here.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



# @receiver(post_save, sender= Project)
def createProject(sender, instance, created, **kwargs):
    print('Instance: ', instance)
    if created:
        print('project created')
    else:
        print('project updated')


post_save.connect(createProject, sender=Project)