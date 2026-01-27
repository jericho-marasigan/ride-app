"""Ride API v1 URL configuration."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ride.api.v1.views import RideViewSet, RideEventViewSet

router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'ride-events', RideEventViewSet, basename='ride-event')

urlpatterns = [
    path('', include(router.urls)),
]
