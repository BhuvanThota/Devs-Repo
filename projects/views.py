from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *
# Create your views here.


def projects(request):
    projectsList = Project.objects.all()
    return render(request, 'projects/projects.html', {'projects' : projectsList})


def project_detail(request, id):
    project = Project.objects.get(id = id)
    star = False
    stars_count = 0
    if request.user.is_authenticated:
        star_projects = request.user.profile.star_projects.all()
        stars_count = len(project.star_profiles.all())
        if project in star_projects:
            star = True
        else:
            star = False

        if request.method == "POST":
            if request.user.profile in project.star_profiles.all():
                project.star_profiles.remove(request.user.profile)  # Remove star
            else:
                project.star_profiles.add(request.user.profile)  
            
            project.save()
            return redirect('project_detail',id = id)
        
    context = {'project' : project, 'star': star, 'stars_count' : stars_count}
    return render(request, 'projects/project_detail.html', context)


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
            return redirect('projects')

    context = {'project_form': project_form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    project_form = ProjectForm(instance= project)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES, instance=project)
        if project_form.is_valid():
            project_form.save()
            return redirect('account')

    context = {'project_form': project_form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)

    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {'object': project}
    return render(request, 'projects/delete_template.html', context)