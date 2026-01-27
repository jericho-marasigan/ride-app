"""Ride API v1 pagination classes."""

from rest_framework.pagination import CursorPagination


class RideCursorPagination(CursorPagination):
    """Cursor pagination for Ride model."""
    
    page_size = 20
    ordering = '-id_ride'  # Newest rides first
    cursor_query_param = 'cursor'


class RideEventCursorPagination(CursorPagination):
    """Cursor pagination for Ride_Event model."""
    
    page_size = 20
    ordering = '-created_at'  # Newest events first
    cursor_query_param = 'cursor'
