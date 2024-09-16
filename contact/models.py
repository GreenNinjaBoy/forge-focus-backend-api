from django.db import models


class contact(models.Model):
    """
    Contact model, adds a contact message
    """
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    message = models.TextField(max_length=250)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message