from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer
from projects.models import *
from users.models import *
# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': 'api/projects'},
        {'GET': 'api/projects/id'},
        {'POST': 'api/projects/id/vote'},
        
        {'POST': 'api/users/token'},
        {'POST': 'api/users/token/refresh'},
    ]

    return Response(routes)



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProjects(request):
    print('USER:', request.user)
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProject(request, id):
    project = Project.objects.get(id = id)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, id):
    project = Project.objects.get(id = id)
    user = request.user.profile
    data = request.data

    print('DATA: ', data)
    
    serializer = ProjectSerializer(project, many=False)

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )

    review.value = data['value']
    review.save()
    project.getVoteCount

    return Response(serializer.data)

