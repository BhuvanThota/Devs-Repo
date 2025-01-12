from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import *
from .forms import *
from .utils import *
# Create your views here.


def projects(request):
    search_query = ''
    projects = Project.objects.filter()

    if request.GET.get('search_query'):
        projects, search_query = searchProjects(request)

    projects, paginator, custom_range = pagination(request, projects, 6)    
    
    context = {'projects' : projects, 'search_query': search_query, 'paginator': paginator, 'custom_range': custom_range}

    return render(request, 'projects/projects.html',context )


def project_detail(request, id):
    project = Project.objects.get(id = id)

    comment_form = ReviewForm()
    
    star, stars_count = star_count_project(request, project)
    
    if request.method == "POST":
        comment_form = ReviewForm(request.POST)
        review = comment_form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        
        #Update the Votes value in Project 
        project.getVoteCount

        messages.success(request, 'Added review successfully!')
        
        return redirect('project_detail', id = id)
    

    context = {'project' : project, 'star': star, 'stars_count' : stars_count, 'comment_form': comment_form}
    return render(request, 'projects/project_detail.html', context)



@login_required(login_url='login')
def toggleStar(request, id):
    profile = request.user.profile
    project = Project.objects.get(id = id)

    if request.method == "POST":
        if profile in project.star_profiles.all():
            project.star_profiles.remove(profile)  # Remove star
            messages.success(request, 'Project Un-Starred!')
        else:
            project.star_profiles.add(profile)  
            messages.success(request, 'Project Starred!')

        
        project.save()

    
    return redirect('project_detail',id = id)



@login_required(login_url='login')
def create_project(request):

    # if not request.user.is_authenticated:
    #     return redirect('login')
    profile =request.user.profile
    project_form = ProjectForm()

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = profile
            project.save()    
 
            projectTags = request.POST['projectTags'].replace(',', ' ').split()
            # print('Project Tags:', projectTags)
            # Adding the tags
            for tag in projectTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            messages.success(request, 'Project was added successfully!')
            return redirect('account')

    page = 'Add Project'
    context = {'project_form': project_form, 'page': page}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    project_form = ProjectForm(instance= project)
    tags = project.tags.all()
    # print('Existing Tags', tags)

    if request.method == 'POST':    
        projectTags = request.POST['projectTags'].replace(',', ' ').split()
        # print('Project Tags:', projectTags)

        project_form = ProjectForm(request.POST, request.FILES, instance=project)
        if project_form.is_valid():
            # Removing the existing tags
            for tag in tags:
                project.tags.remove(tag)
            project_form.save()

            # Adding the updated tags
            for tag in projectTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            messages.success(request, 'Project was updated successfully!')
            return redirect('account')
        

    page = 'Edit Project'
    context = {'project_form': project_form, 'page': page, 'tags': tags}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project was deleted successfully!')
        return redirect('account')

    context = {'object': project}
    return render(request, 'delete_template.html', context)