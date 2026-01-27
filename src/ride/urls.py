"""Ride app URL configuration."""

from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('ride.api.v1.urls')),
]
