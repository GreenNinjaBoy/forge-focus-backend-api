from django.db import models
from django.contrib.auth.models import User

class Goals(models.Model):
    """
    This is the main goals model which will
    store the users chosen goals that they wish to 
    achieve.
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="goals"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    reason = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_pdrfdn', blank=True
    )


class Meta:
    ordering = ['-created_at']

def __str__(self):
    return f'{self.id} {self.name}'