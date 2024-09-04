# models.py
from django.db import models
from goals.models import Goals
from django.contrib.auth.models import User

class Tasks(models.Model):
    """
    This is the main Tasks model
    which will store the users created
    tasks objects
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks")
    goals = models.ForeignKey(
        Goals,
        on_delete=models.CASCADE,
        related_name="tasks_for_goals",
        blank=True,
        null=True)  # Make goals field nullable and optional
    children = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='nested_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    deadline = models.DateTimeField(blank=True, null=True)  # Add deadline field
    task_title = models.CharField(max_length=50)
    task_details = models.CharField(max_length=150, blank=True, null=True)
    value = models.CharField(max_length=150, blank=True, null=True)
    criteria = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.task_title}'