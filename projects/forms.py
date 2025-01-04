from django.forms import ModelForm, widgets
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta():
        model = Project
        fields = ['title', 'description', 'featured_image' , 'demo_link', 'source_link' ]
        # widgets = {
        #     'tags': forms.CheckboxSelectMultiple(),  # Use checkboxes for multiple selections
        # }

        # widgets = {
        #     'tags': forms.CheckboxSelectMultiple(),
        # }


class ReviewForm(ModelForm):
    class Meta():
        model = Review
        fields = ['value', 'body' ]

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment'
        }
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'value':
                field.widget.attrs.update({'class': 'input_vote'})
            else:
                field.widget.attrs.update({'class': 'input_comment'})