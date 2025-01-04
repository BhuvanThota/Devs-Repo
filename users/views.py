from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib import messages
from .models import *
from .forms import *
from .utils import *

# Create your views here.



def loginUser(request):
    page = 'login'
    context = {'page': page }

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except: 
            messages.error(request, 'Username does not exist')


        user = authenticate(request, username = username, password = password)
 
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
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
    search_query = ''
    profiles = Profile.objects.all()

    if request.GET.get('search_query'):
        profiles, search_query = searchProfiles(request)

    profiles, paginator, custom_range = pagination(request, profiles, 6)    

    context = { 'profiles' : profiles, 'search_query': search_query, 'paginator': paginator, 'custom_range': custom_range}
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
    projects = request.user.profile.star_projects.all()
    # if len(star_projects) > 3:
    #     star_projects = star_projects[:3]

    projects, paginator, custom_range = pagination(request, projects, 6)    

    context = {'projects' : projects, 'paginator': paginator, 'custom_range': custom_range}
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


@login_required(login_url = 'login')
def addSkill(request):
    profile = request.user.profile
    skill_form = SkillForm() 

    if request.method == 'POST':
        skill_form = SkillForm(request.POST)
        if skill_form.is_valid():
            skill = skill_form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account') 
    
    page = 'Add Skill'
    context = {'page': page, 'skill_form': skill_form }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url = 'login')
def editSkill(request, id):
    profile = request.user.profile
    skill = profile.skill_set.get(id = id)
    skill_form = SkillForm(instance=skill) 

    if request.method == 'POST':
        skill_form = SkillForm(request.POST, instance=skill)
        if skill_form.is_valid():
            skill_form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account') 
    
    page = 'Edit Skill'
    context = {'page': page, 'skill_form': skill_form }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url = 'login')
def deleteSkill(request, id):
    profile = request.user.profile
    skill = profile.skill_set.get(id = id)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account') 
    

    context = {'object': skill }
    return render(request, 'delete_template.html', context)


@login_required(login_url = 'login')
def inbox(request):
    profile = request.user.profile
    received_messages = profile.received_messages.all()
    unread_messages = received_messages.filter(is_read = False).count()

    context = {"profile": profile, "received_messages": received_messages, "unread_messages": unread_messages}
    return render(request, 'users/inbox.html', context)


@login_required(login_url = 'login')
def single_message(request, id):
    profile = request.user.profile
    single_message = profile.received_messages.get(id = id)

    if single_message.is_read == False:
        single_message.is_read = True
        single_message.save()
    
    context= {"single_message": single_message}
    return render(request, 'users/single_message.html', context)



def message_form(request, id):
    recipient_profile = Profile.objects.get(id = id)
     
    message_form = MessageForm()

    if request.method == "POST":
        message_form = MessageForm(request.POST)

        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.recipient = recipient_profile

            if request.user.is_authenticated:
                sender_profile = request.user.profile
                message.sender = sender_profile
                message.sender_name = sender_profile.name
                message.sender_email = sender_profile.email

            message.save()
            messages.success(request, "Your message was sent successfully!")
        return redirect('user-profile', id = id)

    page = "Send Message"
    context = {"message_form" : message_form, "page": page, "recipient_profile": recipient_profile}
    return render(request, 'users/message_form.html', context)
