from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Tasks
from .serializers import TasksSerializer
from forge_focus_api.permissions import OwnerOnly

class TasksViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user tasks
    """
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]
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
            deadline=timezone.now() + timezone.timedelta(days=7),  # Set deadline to 7 days from now
            completed=False
        )
        serializer = self.get_serializer(new_task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def reset(self, request, pk=None):
        task = self.get_object()
        task.deadline = timezone.now() + timezone.timedelta(days=7)
        task.completed = False
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)