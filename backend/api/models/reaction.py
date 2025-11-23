"""Reaction model for post reactions."""

from django.db import models


class Reaction(models.Model):
    """A reaction to a post (like, useful, funny, etc.)."""

    REACTION_TYPES = [
        ("like", "いいね"),
        ("useful", "参考になった"),
        ("funny", "面白い"),
        ("agree", "同意"),
        ("disagree", "異議"),
    ]

    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="reactions")
    user_session = models.ForeignKey(
        "UserSession",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reactions",
    )
    reaction_type = models.CharField(max_length=20, choices=REACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "board_reaction"
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"
        unique_together = [["post", "user_session", "reaction_type"]]
        indexes = [
            models.Index(fields=["post", "reaction_type"]),
        ]

    def __str__(self):
        return f"{self.reaction_type} on Post #{self.post.post_number}"
