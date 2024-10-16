from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerUser, name = 'register'),

    path('', views.profiles, name='profiles'),
    path('profile/<str:id>', views.userprofile, name='user-profile'),
    
    path('account', views.account, name='account'),
    path('edit-account', views.editAccount, name='edit-account'),
    
    path('starred', views.starred, name='starred'),
    
]