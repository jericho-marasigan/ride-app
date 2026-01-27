"""Ride API v1 custom managers."""

from django.db import models
from django.utils import timezone


class TodayEventsManager(models.Manager):
    """Manager to get only today's events."""
    
    def get_queryset(self):
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        return super().get_queryset().filter(
            created_at__gte=today_start,
            created_at__lte=today_end
        )


__all__ = ['TodayEventsManager']
