from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from .serializers import TaskSerializer, TasklistSerializer, TagSerializer, UserCreateSerializer, UserSerializer #UserLoginSerializer,
from .models import Task, Tasklist, Tag
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .permissions import IsOwner
from django.http import Http404
from django.db.models import Q


#User = settings.AUTH_USER_MODEL
User = get_user_model()


class TasklistCreateView(generics.ListCreateAPIView):
    serializer_class = TasklistSerializer
    permission_classes = (IsAuthenticated,)
    #permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        owner = self.request.user
        serializer.save(owner=owner)


    def get_queryset(self):
        queryset = Tasklist.objects.all()
        #self.check_object_permissions(self.request, queryset)
        #return queryset
        owner_id = self.request.user.id
        if owner_id is not None:
            queryset = queryset.filter(owner_id= owner_id)

            return queryset
        else:

            return None




class TasklistDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TasklistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Tasklist.objects.all()
        owner_id = self.request.user.id
        if owner_id is not None:
            queryset = queryset.filter(owner_id= owner_id)

            return queryset
        else:

            return None


class TaskCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            taskslist_id = Tasklist.objects.filter(owner= self.request.user)
            #user_shared = Tasklist.objects.filter(shared=self.request.user)
            #queryset = Task.objects.filter(Q(tasklist_id__in= taskslist_id) | Q(tasklist_id__in= user_shared))
            queryset = Task.objects.filter(tasklist_id__in=taskslist_id)
        except:
            queryset = None
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None and queryset is not None:
            queryset = queryset.filter(tasklist_id = list_id)
        else:
            raise Http404("U must be the owner")
        return queryset

    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id', None)
        try:
            tasklist = Tasklist.objects.filter(owner = self.request.user).get(pk=list_id)
        except Tasklist.DoesNotExist:
            raise Http404("u must be the owner")
        serializer.save(tasklist=tasklist)


class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            user_tasks = Tasklist.objects.filter(owner= self.request.user)
            queryset = Task.objects.filter(tasklist_id__in=user_tasks)
        except:
            queryset = None
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None and queryset is not None:
            queryset = queryset.filter(tasklist_id = list_id)
        if not queryset:
            raise Http404("U must be the owner")
        return queryset


class TagCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = TagSerializer


class TagDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]


"""class UserLoginView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data= data)
        if serializer.is_valid(raise_exception= True):
            new_data = serializer.data
            return Response(new_data, status= HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)"""


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
