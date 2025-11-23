"""UserSession model for tracking anonymous users."""

import uuid

from django.db import models


class UserSession(models.Model):
    """Anonymous user session for tracking activity."""

    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    temporary_name = models.CharField(
        max_length=100, help_text="Auto-generated name like 'ID:abc123'"
    )
    post_count = models.IntegerField(default=0)
    thread_count = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "board_user_session"
        ordering = ["-last_activity_at"]
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"
        indexes = [
            models.Index(fields=["session_id"]),
            models.Index(fields=["-total_points"]),
        ]

    def __str__(self):
        return self.temporary_name
