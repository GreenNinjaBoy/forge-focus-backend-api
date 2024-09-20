from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from forge_focus_api.permissions import OwnerOnly
from .models import Tasks
from .serializers import TasksSerializer

class FilterList(filters.BaseFilterBackend):
    """
    Custom filter to allow users to filter tasks by goal_id, parent_id, and parent
    """
    def filter_queryset(self, request, queryset, view):
        goal_id = request.query_params.get('goal_id')
        parent_id = request.query_params.get('parent_id')
        parent = request.query_params.get('parent')
        
        if goal_id:
            queryset = queryset.filter(goals_id=goal_id)
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        if parent:
            queryset = queryset.filter(parent=None)
        
        return queryset

class TasksList(generics.ListCreateAPIView):
    """
    API view to retrieve list of tasks or create a new task
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TasksSerializer
    filter_backends = [FilterList]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.tasks.all().order_by('deadline', 'created_at')
        else:
            return Tasks.objects.none()

class TasksViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user tasks
    """
    serializer_class = TasksSerializer
    permission_classes = [OwnerOnly]
    queryset = Tasks.objects.all()

    def get_queryset(self):
        return Tasks.objects.filter(owner=self.request.user)

    @action(detail=True, methods=['patch'])
    def toggle_complete(self, request, pk=None):
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reuse(self, request, pk=None):
        original_task = self.get_object()
        new_task = Tasks.objects.create(
            owner=self.request.user,
            goals=original_task.goals,
            task_title=original_task.task_title,
            task_details=original_task.task_details,
            deadline=None,  
            completed=False
        )
        serializer = self.get_serializer(new_task)
        return Response(serializer.data)