from rest_framework import serializers
from .models import Goals
from tasks.models import Tasks
from tasks.serializers import TasksSerializer


class GoalsSerializer(serializers.ModelSerializer):
    """
    This is the serializer for the goals model. It will change the
    owner.id into owner.username. It will add an extra field 'is_owner'.
    The serializer will prevent large images from being saved to the
    database and changes the date fields into an easier format.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    tasks = TasksSerializer(many=True, read_only=True,
                            source='tasks_for_goals')
    image = serializers.ImageField(required=False)
    image_url = serializers.SerializerMethodField()

    def validate_image(self, value):
        """
        This is a custom validation method used
        for the image field.
        This was taken from the Django rest walkthrough
        """

        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Sorry but the Image size is larger than 2mb!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Sorry but the image width is larger than 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Sorry but the image height is larger than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return 'https://res.cloudinary.com/dcnhbmqy4/image/upload/v1713429424/media/images/default_post_pdrfdn.jpg'

    class Meta:
        model = Goals
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'name',
            'reason',
            'image',
            'image_url',
            'is_owner',
            'tasks',
            'tasks_for_goals',
        ]