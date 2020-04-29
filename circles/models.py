from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model


class Event(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    start = models.DateTimeField()

    participants = models.ManyToManyField(get_user_model(), related_name="events")

    def is_full(self):
        """determines wether event is already full (7 participants)"""
        return len(self.participants) >= 7  # TODO: untested

    def __str__(self) -> str:
        return str(self.start)

    class Meta:
        ordering = ("start",)
