from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Goals(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="goals"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    reason = models.TextField(blank=True, null=True)
    image = CloudinaryField(
        'image',
        folder='goals_images',
        default='media/images/default_post_pdrfdn',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.name}'