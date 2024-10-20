from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.projects, name="projects"),
    path('project_detail/<str:id>/', views.project_detail, name="project_detail"),

    path('create_project/', views.create_project, name="create_project"),
    path('update_project/<str:id>/', views.update_project, name="update_project"),
    path('delete_project/<str:id>/', views.delete_project, name="delete_project"),

    path('toggle_star/<str:id>/', views.toggleStar, name= 'toggle_star')
]