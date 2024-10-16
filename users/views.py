from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from .forms import CustomUserCreationForm

# Create your views here.



def loginUser(request):
    page = 'login'
    context = {'page': page }

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except: 
            messages.error(request, 'Username does not exist')


        user = authenticate(request, username = username, password = password)
 
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('login')

    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was successfully logged out!')

    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    context = {'page': page, 'form': form }

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User Account was Successfully Created!')

            login(request, user)
            return redirect('edit-account')
        
        else:
            messages.error(request, 'An error has occured during registration')


    return render(request, 'users/login_register.html', context)



def profiles(request):
    profiles = Profile.objects.all()
    context = { 'profiles' : profiles}
    return render(request, 'users/profiles.html', context)


def userprofile(request, id):
    profile = Profile.objects.get(id= id)
    topSkills = profile.skill_set.exclude(description__exact = '')
    otherSkills = profile.skill_set.filter(description__exact = '')
    
    context = {'profile' : profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user_profile.html', context)


@login_required(login_url = 'login')
def account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile' : profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url = 'login')
def starred(request):
    star_projects = request.user.profile.star_projects.all()
    if len(star_projects) > 3:
        star_projects = star_projects[:3]
    context = {'star_projects': star_projects}
    return render(request, 'users/starred.html', context)


@login_required(login_url = 'login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile )
        if form.is_valid():
            form.save()
            return redirect('account')
        
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)