from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm
from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']

        labels = {
            'first_name' : 'Name',
            'email' : 'Email',
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'name', 'location', 'email', 'short_intro',
                  'bio', 'profile_image', 'social_github', 'social_leetcode', 
                  'social_linkedin', 'social_twitter', 'social_website']
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != 'profile_image':
                field.widget.attrs.update({'class': 'added_input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']




class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['sender_name', 'sender_email', 'subject', 'body']

        labels = {
            'sender_name' : 'Your Name',
            'sender_email' : 'Email',
        }
