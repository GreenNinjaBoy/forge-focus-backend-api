from django.db import models
from goals.model import Goals
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
        related_name="tasks_for_goals")
    children = models.BooleanField(default=False)
    parent = models.Foreignkey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='nested_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    deadline = models.BooleanField(default=True)
    task_title = models.CharField(max_length=50)
    task_details = models.CharField(max_lenght=150, blank=True, null=True)
    value = models.CharField(max_lenght=150, blank=True, null=True)
    criteria = models.CharField( max_lenght=150, blank=true, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.goal_title}'
