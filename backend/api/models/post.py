"""掲示板のレス（投稿）モデル.

スレッド内の個別の投稿（レス）を管理する。
アンカー機能や返信機能をサポートする。
"""

from django.db import models


class Post(models.Model):
    """スレッド内のレス（投稿）を表すモデル.

    スレッド内の個別の投稿を保持する。
    レス番号による順序管理と、アンカー機能のための返信元参照をサポートする。

    Attributes:
        thread: 所属スレッド（削除時はカスケード削除）
        author_session: 投稿者のセッション（削除時はNULLに設定）
        content: 投稿本文
        post_number: スレッド内のレス番号（1から始まる連番）
        reply_to: 返信元のレス（アンカー機能用）
        is_op: 最初の投稿（OP）かどうか
        created_at: 投稿日時
        updated_at: 更新日時
    """

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

    def __str__(self) -> str:
        """レスの文字列表現を返す.

        Returns:
            レス番号とスレッドタイトルの組み合わせ
        """
        return f"Post #{self.post_number} in {self.thread.title}"
