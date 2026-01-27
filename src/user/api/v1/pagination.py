"""User API v1 pagination classes."""

from rest_framework.pagination import CursorPagination


class UserCursorPagination(CursorPagination):
    """Cursor pagination for User model."""
    
    page_size = 20
    ordering = '-id_user'  # Newest users first
    cursor_query_param = 'cursor'
