"""Ride API v1 filters."""

from django_filters import rest_framework as filters
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Radians, Sin
from ride.api.v1.models import Ride, Ride_Event


class RideFilter(filters.FilterSet):
    """Filter for Ride model."""
    
    status = filters.ChoiceFilter(
        field_name='status',
        choices=Ride.Status.choices,
    )
    rider_email = filters.CharFilter(
        field_name='id_rider__email',
        lookup_expr='iexact',
    )
    ordering = filters.OrderingFilter(
        fields=(
            ('pickup_time', 'pickup_time'),
        ),
    )
    pickup_lat = filters.NumberFilter(method='filter_by_distance', label='Pickup Latitude')
    pickup_lon = filters.NumberFilter(method='filter_by_distance', label='Pickup Longitude')
    
    class Meta:
        model = Ride
        fields = ['status', 'rider_email']
    
    def filter_by_distance(self, queryset, name, value):
        """
        Calculate distance from given coordinates using Haversine formula.
        Requires both pickup_lat and pickup_lon query parameters.
        Orders results by distance ascending.
        """
        pickup_lat = self.request.query_params.get('pickup_lat')
        pickup_lon = self.request.query_params.get('pickup_lon')
        
        if pickup_lat is None or pickup_lon is None:
            return queryset
        
        try:
            lat = float(pickup_lat)
            lon = float(pickup_lon)
        except (ValueError, TypeError):
            return queryset
        
        # Haversine formula for distance calculation
        # Distance in kilometers (Earth radius = 6371 km)
        distance = ExpressionWrapper(
            6371 * ACos(
                Cos(Radians(lat)) * 
                Cos(Radians(F('pickup_latitude'))) * 
                Cos(Radians(F('pickup_longitude')) - Radians(lon)) +
                Sin(Radians(lat)) * 
                Sin(Radians(F('pickup_latitude')))
            ),
            output_field=FloatField()
        )
        
        return queryset.annotate(distance=distance).order_by('distance')


class RideEventFilter(filters.FilterSet):
    """Filter for Ride_Event model."""
    
    ride_id = filters.NumberFilter(
        field_name='id_ride_id',
    )
    
    class Meta:
        model = Ride_Event
        fields = ['ride_id']
