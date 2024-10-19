from .models import *

# Create your models here.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



@receiver(post_save, sender= Review)
def createProject(sender, instance, created, **kwargs):
    print('Instance: ', instance)
    
