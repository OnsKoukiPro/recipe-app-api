"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers  #serializers take json input, validates it, and converts it to a python object or model


class UserSerializer(serializers.ModelSerializer): #model serializers, saves and modifies the model directly
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)