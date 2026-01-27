"""Ride API v1 models."""

from django.db import models
from user.api.v1.models import User
from ride.api.v1.managers import TodayEventsManager


class Ride(models.Model):
    """Ride model for tracking ride requests and status."""
    
    class Status(models.TextChoices):
        EN_ROUTE = 'en-route', 'En Route'
        PICKUP = 'pickup', 'Pickup'
        DROPOFF = 'dropoff', 'Dropoff'
    
    id_ride = models.AutoField(primary_key=True, db_column='id_ride')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
    )
    id_rider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rides_as_rider',
        db_column='id_rider',
    )
    id_driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rides_as_driver',
        db_column='id_driver',
    )
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()
    
    class Meta:
        db_table = 'ride'
        verbose_name = 'Ride'
        verbose_name_plural = 'Rides'
        indexes = [
            models.Index(fields=['pickup_latitude', 'pickup_longitude'], name='ride_pickup_coords'),
            models.Index(fields=['dropoff_latitude', 'dropoff_longitude'], name='ride_dropoff_coords'),
        ]
    
    def __str__(self):
        return f"Ride {self.id_ride} - {self.get_status_display()}"


class Ride_Event(models.Model):
    """Ride Event model for tracking ride event history."""
    
    id_ride_event = models.AutoField(primary_key=True, db_column='id_ride_event')
    id_ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name='events',
        db_column='id_ride',
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()
    todays = TodayEventsManager()
    
    class Meta:
        db_table = 'ride_event'
        verbose_name = 'Ride Event'
        verbose_name_plural = 'Ride Events'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Event {self.id_ride_event} for Ride {self.id_ride_id}"


__all__ = ['Ride', 'Ride_Event']