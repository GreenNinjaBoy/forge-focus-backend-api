from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import Tasks
from .serializers import TasksSerializer
from rest_framework import generics, filters

class FilterList(filters.BaseFilterBackend):
    """
    This is a custom filter which will
    allow the user to filter their tasks
    by goal_id, no parent and parent_id
    """

    def filter_queryset(self, request, queryset, view):
        goal_id = request.query_params.get('goal_id')
        parent_id = request.query_params.get('parent_id')
        parent = request.query_params.get('parent')
        if goal_id:
            queryset = queryset.filter(goal_id=goal_id)
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        if parent:
            queryset = queryset.filter(parent=None)
        return queryset

class TasksList(generics.ListCreateAPIView):
    """
    This view will return to a logged in user
    a list of tasks that they have created and 
    also allow that user to create new tasks
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TasksSerializer
    filter_backends = [
        FilterList
    ]

    def perform_create(self, serializer):
        """
        This will add the owner data to 
        the object before it is saved
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Pulls all of the task instances that are linked
        to the currently logged in user. This will be in
        order of rank and then by created_at
        """
        if self.request.user.is_authenticated:
            return self.request.user.usertasks.all().order_by('deadline', 'created_at')
        else:
            return UserTasks.objects.none()

class UserTasksDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    View to return a specific user task where the
    pk will be the id of the user task
    """ 

    serializer_class = UserTasksSerializer
    permission_classes = [OwnerOnly]
    queryset = UserTasks.objects.all()
     



