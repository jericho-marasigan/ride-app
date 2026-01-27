"""Ride API v1 serializers."""

from rest_framework import serializers
from ride.api.v1.models import Ride, Ride_Event
from user.api.v1.serializers import UserSerializer


class RideEventSerializer(serializers.ModelSerializer):
    """Serializer for Ride_Event model."""
    
    class Meta:
        model = Ride_Event
        fields = [
            'id_ride_event',
            'id_ride',
            'description',
            'created_at',
        ]
        read_only_fields = ['id_ride_event', 'created_at']


class RideSerializer(serializers.ModelSerializer):
    """Serializer for Ride model."""
    
    rider = UserSerializer(source='id_rider', read_only=True)
    driver = UserSerializer(source='id_driver', read_only=True)
    events = RideEventSerializer(many=True, read_only=True)
    
    class Meta:
        model = Ride
        fields = [
            'id_ride',
            'status',
            'id_rider',
            'id_driver',
            'rider',
            'driver',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
            'events',
        ]
        read_only_fields = ['id_ride']


class RideCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new rides."""
    
    class Meta:
        model = Ride
        fields = [
            'id_ride',
            'status',
            'id_rider',
            'id_driver',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
        ]
        read_only_fields = ['id_ride']


__all__ = ['RideSerializer', 'RideCreateSerializer', 'RideEventSerializer']