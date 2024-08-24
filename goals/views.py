from forge_focus_api.permissions import OwnerOnly
from .serializers import GoalsSerializer
from .models import Goals
from rest_framework import generics, permissions

class GoalsList(generics.ListCreateAPIView):
    """
     This view will return a list of goals area for the
     logged in user, will also provide the user a new
     area to create new goals.
    """
    serializer_class = GoalsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        This will add the owner data to the Goals object
        before it is saved.
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This will pull all the Goals instances that are only linked
        to the current user. Within this order will be rank first 
        (with null last), and then created_at.
        """
        if self.request.user.is_authenticated:
            return self.request.user.goals.all().order_by('created_at')
        else:
            return Goals.objects.none() 

class GoalsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This view will return a specific goal where 
    pk will be the ID of the goal.
    """
    serializer_class = GoalsSerializer
    permission_classes = [OwnerOnly]
    queryset = Goals.objects.all()