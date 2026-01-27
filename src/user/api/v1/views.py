"""User API v1 views."""

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from user.api.v1.models import User
from user.api.v1.serializers import UserSerializer, UserCreateSerializer
from user.api.v1.pagination import UserCursorPagination


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = UserCursorPagination
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer