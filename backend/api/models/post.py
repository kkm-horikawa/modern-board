"""Post model for thread messages."""

from django.db import models


class Post(models.Model):
    """A post/message in a thread."""

    thread = models.ForeignKey("Thread", on_delete=models.CASCADE, related_name="posts")
    author_session = models.ForeignKey(
        "UserSession",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    content = models.TextField()
    post_number = models.IntegerField(
        help_text="Sequential number within the thread (e.g., >>123)"
    )
    reply_to = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replies",
        help_text="Reference to another post being replied to",
    )
    is_op = models.BooleanField(
        default=False, help_text="True if this is the original post (first post)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "board_post"
        ordering = ["post_number"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        unique_together = [["thread", "post_number"]]
        indexes = [
            models.Index(fields=["thread", "post_number"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Post #{self.post_number} in {self.thread.title}"
