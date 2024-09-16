from rest_framework import serializers
from contact.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the contact model
    """

    class Meta:
        model = Contact
        fields = ['id', 'created_at', 'name', 'email', 'message']