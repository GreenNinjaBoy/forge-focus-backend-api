from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Tasks
from .serializers import TasksSerializer
from forge_focus_api.permissions import OwnerOnly


class TasksViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user tasks.
    Provides default CRUD operations and custom actions
    for toggling task completion,
    reusing tasks, and resetting task deadlines.
    """
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]
    queryset = Tasks.objects.all()

    def perform_create(self, serializer):
        """
        Save the new task instance with the owner set to the current user.
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Return the queryset of tasks filtered by the current user.
        """
        return Tasks.objects.filter(owner=self.request.user)

    @action(detail=True, methods=['patch'])
    def toggle_complete(self, request, pk=None):
        """
        Toggle the completion status of a task.
        """
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reuse(self, request, pk=None):
        """
        Create a new task based on an existing task,
        with a new deadline set to 7 days from now.
        """
        original_task = self.get_object()
        new_task = Tasks.objects.create(
            owner=self.request.user,
            goals=original_task.goals,
            task_title=original_task.task_title,
            task_details=original_task.task_details,
            deadline=timezone.now() + timezone.timedelta(days=7),
            completed=False
        )
        serializer = self.get_serializer(new_task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def reset(self, request, pk=None):
        """
        Reset the deadline of a task to 7 days from now
        and mark it as not completed.
        """
        task = self.get_object()
        task.deadline = timezone.now() + timezone.timedelta(days=7)
        task.completed = False
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)


class TasksList(generics.ListCreateAPIView):
    """
    API view to retrieve a list of tasks or create a new task.
    """
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]

    def get_queryset(self):
        """
        Return the queryset of tasks filtered by the current user.
        """
        return Tasks.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Save the new task instance with the owner set to the current user.
        """
        serializer.save(owner=self.request.user)
