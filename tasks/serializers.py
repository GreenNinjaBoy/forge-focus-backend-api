from django.utils import timezone
from . models import UserGoals
from rest_framework import serializers

class TasksSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    deadline_near = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user == obj.owner
        return False

    def get_time_remaining(self, obj):
        future_deadline = obj.deadline
        if future_deadline:
           today_aware = timezone.now()
           day_remaining = (future_deadline - today_aware).days
           return days_remaining
        return None 

    def get_deadline_near(self, obj):
        days_remaining = self.get_time_remaining(obj)
        return days_remaining is not None and days_remaining <=7

    
    class Meta:
        model = Tasks
        field = [
            'id', 'owner', 'is_owner', 'goals', 'children', 'parent',
            'created_at', 'update_at', 'active', 'deadline', 'task_title',
            'task_details', 'criteria', 'deadline_near', 'time_remaining',
        ]

