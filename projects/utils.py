from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    Tags = Tag.objects.filter(name__icontains = search_query)

    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) |
                                                 Q(owner__name__icontains= search_query)|
                                                 Q(tags__in=Tags))

    return projects, search_query


def pagination(request, projects, results = 6):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    left_index = max(int(page)-3 , 1)
    right_index = min(int(page)+4, paginator.num_pages+1)

    custom_range = range(left_index,right_index)

    return projects, paginator, custom_range





