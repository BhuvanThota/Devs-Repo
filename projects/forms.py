from django.forms import ModelForm, widgets
from django import forms
from .models import Project


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['owner'].initial = user

    class Meta():
        model = Project
        fields = ['owner','title', 'description', 'featured_image' , 'demo_link', 'source_link', 'tags' ]
        widgets = {
            'owner': forms.HiddenInput(),  # Makes the 'owner' field a hidden input
        }

        # widgets = {
        #     'tags': forms.CheckboxSelectMultiple(),
        # }

