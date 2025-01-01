from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns =  [
    path('', views.getRoutes, name='api_home'),
    
    path('projects/', views.getProjects, name='api_projects'),
    path('project/<str:id>', views.getProject, name='api_single_project'),
    path('project/<str:id>/vote', views.projectVote, name='api_project_vote'),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]