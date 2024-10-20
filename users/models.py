from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True, default='India')
    email = models.EmailField(max_length=500, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/default-profile-image.png' )
    
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_leetcode = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField( default = uuid.uuid4, unique = True, primary_key = True, editable = False)

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['created']



class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField( default = uuid.uuid4, unique = True, primary_key = True, editable = False)

    def __str__(self):
        return self.name



class Message(models.Model):
    sender = models.ForeignKey(Profile, 
                               on_delete=models.SET_NULL, null = True, 
                               blank= True, related_name = "sent_messages" )
    recipient = models.ForeignKey(Profile, 
                                  on_delete=models.SET_NULL, null = True, 
                                  blank= True, related_name = "received_messages" )
    sender_name = models.CharField(max_length=200, null = True, blank = True)
    sender_email = models.EmailField(max_length=200, null = True, blank = True)
    subject = models.CharField(max_length=200, null = True, blank = True)
    body = models.TextField()
    is_read = models.BooleanField(default = False, null = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField( default = uuid.uuid4, unique = True, primary_key = True, editable = False)

    def __str__(self):
        return f"{self.sender} - {self.subject[:20]} "
    
    class Meta:
        ordering = ['is_read', '-created']
