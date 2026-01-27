"""User API v1 views."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.api.v1.models import User
from user.api.v1.serializers import UserSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """Allow anyone to create a user, but require authentication for other actions."""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]