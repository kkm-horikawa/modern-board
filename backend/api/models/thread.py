"""Thread model for bulletin board threads."""

from django.db import models


class Thread(models.Model):
    """A discussion thread on the bulletin board."""

    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="threads"
    )
    tags = models.ManyToManyField("Tag", blank=True, related_name="threads")
    author_session = models.ForeignKey(
        "UserSession",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="authored_threads",
    )
    post_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    momentum = models.FloatField(
        default=0.0, help_text="Momentum score based on recent activity"
    )
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_post_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "board_thread"
        ordering = ["-is_pinned", "-last_post_at"]
        verbose_name = "Thread"
        verbose_name_plural = "Threads"
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["-momentum"]),
            models.Index(fields=["category", "-last_post_at"]),
        ]

    def __str__(self):
        return self.title
