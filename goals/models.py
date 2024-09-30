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

    def get_image(self):
        if self.image:
            return f"{settings.API_URL}/media/{self.image.name}"
        return f"{settings.API_URL}/media/images/default_post_pdrfdn"

    # The Meta class is indented to be inside the Goals class
    # because it provides metadata specifically for the Goals model.
    # This indentation indicates that Meta is an inner class of Goals.
    # Django looks for this inner Meta class
    # to configure model-specific settings like ordering.
    class Meta:
        ordering = ['-created_at']

    # The __str__ method is indented to be inside the Goals class because it's
    # a method that belongs to the Goals model. In Python, all methods that are
    # part of a class must be indented within that class.
    # This indentation tells Python that this method is associated
    # with the Goals class and should be
    # called on Goals instances.
    def __str__(self):
        return f'{self.id} {self.name}'
