from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    Skills = Skill.objects.filter(name__icontains = search_query)

    profiles = Profile.objects.distinct().filter(Q(name__icontains = search_query) | 
                                      Q(short_intro__icontains = search_query) |
                                      Q(skill__in=Skills))

    return profiles, search_query


def pagination(request, query_set, results = 6):
    page = request.GET.get('page')
    paginator = Paginator(query_set, results)
    
    try:
        query_set = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        query_set = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        query_set = paginator.page(page)

    left_index = max(int(page)-3 , 1)
    right_index = min(int(page)+4, paginator.num_pages+1)

    custom_range = range(left_index,right_index)

    return query_set, paginator, custom_range