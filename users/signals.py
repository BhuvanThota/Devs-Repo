from django.contrib.auth.models import User
from .models import *
# Create your models here.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    print('User Saved! Profile Trigger!')
    print('Instance: ', instance)
    print('Created: ', created)
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    print('Deleting User: ', instance)
    user = instance.user
    user.delete()


post_save.connect(updateUser, sender=Profile)
post_save.connect(createProfile, sender=User)


