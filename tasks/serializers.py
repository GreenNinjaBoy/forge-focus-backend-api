from rest_framework import serializers
from .models import Tasks
from django.utils import timezone


class TasksSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tasks model.
    Includes additional fields for the owner's username, ownership status,
    time remaining until the deadline, and whether the deadline is near.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    deadline_near = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Determine if the current user is the owner of the task.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user == obj.owner
        return False

    def get_time_remaining(self, obj):
        """
        Calculate the number of days remaining until the task's deadline.
        """
        future_deadline = obj.deadline
        if future_deadline:
            today_aware = timezone.now()
            days_remaining = (future_deadline - today_aware).days
            return days_remaining
        return None

    def get_deadline_near(self, obj):
        """
        Determine if the task's deadline is within the next 7 days.
        """
        days_remaining = self.get_time_remaining(obj)
        return days_remaining is not None and days_remaining <= 7

    class Meta:
        """
        Meta class for the TasksSerializer.
        Defines the model and fields to be serialized.
        """
        model = Tasks
        fields = [
            'id', 'owner', 'is_owner', 'goals', 'children', 'parent',
            'created_at', 'updated_at', 'active', 'deadline', 'task_title',
            'task_details', 'criteria', 'deadline_near', 'time_remaining',
            'completed',
        ]
        read_only_fields = ['owner', 'is_owner', 'created_at', 'updated_at']
