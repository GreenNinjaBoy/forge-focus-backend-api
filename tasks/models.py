from django.db import models
from goals.models import Goals
from django.contrib.auth.models import User


class Tasks(models.Model):
    """
    Model representing a task.
    A task can be associated with a goal and can have nested sub-tasks.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name="tasks")
    goals = models.ForeignKey(Goals, on_delete=models.CASCADE,
                              related_name="tasks_for_goals",
                              blank=True, null=True)
    children = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name='nested_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    deadline = models.DateTimeField(blank=True, null=True)
    task_title = models.CharField(max_length=50)
    task_details = models.CharField(max_length=150, blank=True, null=True)
    value = models.CharField(max_length=150, blank=True, null=True)
    criteria = models.CharField(max_length=150, blank=True, null=True)
    completed = models.BooleanField(default=False)

    class Meta:
        """
        Meta class for the Tasks model.
        Defines the default ordering for the model.
        """
        ordering = ['-created_at']

    def __str__(self):
        """
        String representation of the task.
        """
        return f'{self.id} {self.task_title}'
