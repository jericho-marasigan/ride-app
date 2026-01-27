"""User API v1 serializers."""

from rest_framework import serializers
from user.api.v1.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = [
            'id_user',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone_number',
        ]
        read_only_fields = ['id_user']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users."""
    
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'id_user',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'role',
            'phone_number',
        ]
        read_only_fields = ['id_user']
    
    def create(self, validated_data):
        """Create a new user with encrypted password."""
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


__all__ = ['UserSerializer', 'UserCreateSerializer']