from django.db import models

import uuid
from users.models import Profile, Skill
# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.TextField(null = True, blank = True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg" )
    demo_link = models.CharField(max_length = 2000, null = True, blank = True)
    source_link = models.CharField(max_length = 2000, null = True, blank = True )
    vote_total = models.IntegerField(default=0, null = True, blank = True)
    vote_ratio = models.IntegerField(default=0, null = True, blank = True)
    tags = models.ManyToManyField('Tag', blank = True) 
    star_profiles = models.ManyToManyField(Profile, blank = True, related_name='star_projects')
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField( default = uuid.uuid4, unique = True, primary_key = True, editable = False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio','-vote_total', '-created']
    
    @property
    def imageURL(self):
        try:
            return self.featured_image.url
        except:
            return 'images/default.jpg'

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()

        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes/totalVotes) * 100

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()



class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    body = models.TextField(null = True, blank = True)
    value = models.CharField(max_length= 200, choices=VOTE_TYPE, default='up')
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField( default = uuid.uuid4, unique = True, primary_key = True, editable = False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return f"{self.value} - {self.project.title[:15]} - {self.owner.username[:15]} "
    




class Tag(models.Model):
    name = models.CharField(max_length = 200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key= True, editable= False)


    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

