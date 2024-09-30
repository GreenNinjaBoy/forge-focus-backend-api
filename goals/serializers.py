"""Serializer for the Goals model."""
from rest_framework import serializers
from cloudinary.models import CloudinaryField
from .models import Goals
from tasks.serializers import TasksSerializer


class GoalsSerializer(serializers.ModelSerializer):
    """
    Serializer for the goals model.

    Changes the owner.id into owner.username and adds an extra field
    'is_owner'.Prevents large images from being saved to the database
    and changes the date fields into an easier format.
    """

    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    tasks = TasksSerializer(
        many=True, read_only=True, source='tasks_for_goals')
    image = serializers.ImageField(required=False)
    image_url = serializers.SerializerMethodField()

    def validate_image(self, value):
        """
        Custom validation method for the image field.

        Taken from the Django REST framework walkthrough.
        """
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size is larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width is larger than 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height is larger than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        """Check if the requesting user is the owner of the goal."""
        request = self.context['request']
        return request.user == obj.owner

    def get_image_url(self, obj):
        """Get the URL of the image, or return a default if not available."""
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return ('https://res.cloudinary.com/dcnhbmqy4/image/upload/'
                'v1713429424/media/images/default_post_pdrfdn.jpg')

    class Meta:
        """Meta class to specify model and fields."""
        model = Goals
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'reason',
            'image', 'image_url', 'is_owner', 'tasks', 'tasks_for_goals',
        ]
