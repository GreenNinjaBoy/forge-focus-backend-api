from rest_framework import serializers
from django.contrib.auth.models import User

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser')
        read_only_fields = ('is_superuser',)