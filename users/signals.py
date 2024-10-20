from django.contrib.auth.models import User
from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail

from .models import *
from projects.models import *
# Create your models here.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



@receiver(post_save, sender=User)
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

        EMAIL_HOST_USER = settings.EMAIL_HOST_USER
        subject = "Welcome to DEVSREPO"
        message = "You have successfully created account in DevsRepo. Please update your profile."

        if user.email is not None:
            try:    
                send_mail(
                    subject,
                    message,
                    EMAIL_HOST_USER,
                    [user.email,],
                    fail_silently=False,
                )
                print('Email sent successfully', user.email)
            except:
                pass
                
        

@receiver(post_save, sender=Profile)
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



# Not to you as the tags are reflected for all the users not for individual account unlike skills.

# @receiver(post_save, sender=Skill)
# def add_default_tag(sender, instance, created, **kwargs):
#     if created:
#         normalized_name = instance.name.lower()
#         tag, created = Tag.objects.get_or_create(
#             name = normalized_name,
#         )

# @receiver(post_delete, sender=Skill)
# def delete_related_tag(sender, instance, **kwargs):
#     try:
#         # Perform case-insensitive lookup to delete the corresponding tag
#         tag = Tag.objects.get(name__iexact=instance.name)
#         tag.delete()
#     except Tag.DoesNotExist:
#         pass 