"""Ride API v1 views."""

from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ride.api.v1.models import Ride, Ride_Event
from ride.api.v1.serializers import (
    RideSerializer,
    RideCreateSerializer,
    RideEventSerializer,
)
from ride.api.v1.pagination import RideCursorPagination, RideEventCursorPagination
from ride.api.v1.filters import RideFilter, RideEventFilter


class RideViewSet(viewsets.ModelViewSet):
    """ViewSet for Ride model."""
    
    def get_queryset(self):
        """Return queryset with optimized prefetch for today's events."""
        return Ride.objects.select_related(
            'id_rider', 'id_driver'
        ).prefetch_related(
            Prefetch(
                'events',
                queryset=Ride_Event.todays.all(),
                to_attr='todays_ride_events'
            )
        ).all()
    permission_classes = [IsAdminUser]
    pagination_class = RideCursorPagination
    filterset_class = RideFilter
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'create':
            return RideCreateSerializer
        return RideSerializer


class RideEventViewSet(viewsets.ModelViewSet):
    """ViewSet for Ride_Event model."""
    
    queryset = Ride_Event.objects.select_related('id_ride').all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUser]
    pagination_class = RideEventCursorPagination
    filterset_class = RideEventFilter