from .models import *
from django.db.models import Q

def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    Tags = Tag.objects.filter(name__icontains = search_query)

    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) |
                                                 Q(owner__name__icontains= search_query)|
                                                 Q(tags__in=Tags))

    return projects, search_query





