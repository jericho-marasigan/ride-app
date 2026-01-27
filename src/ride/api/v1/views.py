"""Ride API v1 views."""

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ride.api.v1.models import Ride, Ride_Event
from ride.api.v1.serializers import (
    RideSerializer,
    RideCreateSerializer,
    RideEventSerializer,
)


class RideViewSet(viewsets.ModelViewSet):
    """ViewSet for Ride model."""
    
    queryset = Ride.objects.select_related(
        'id_rider', 'id_driver'
    ).prefetch_related('events').all()
    permission_classes = [IsAdminUser]
    
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
    
    def get_queryset(self):
        """Filter events by ride_id if provided in query params."""
        queryset = super().get_queryset()
        ride_id = self.request.query_params.get('ride_id')
        if ride_id is not None:
            queryset = queryset.filter(id_ride_id=ride_id)
        return queryset