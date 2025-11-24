"""レスへのリアクションモデル.

レスに対するリアクション（いいね、面白いなど）を管理する。
同一セッションからの重複リアクションを防止する。
"""

from django.db import models


class Reaction(models.Model):
    """レスへのリアクションを表すモデル.

    レスに対するユーザーの反応を記録する。
    リアクションタイプは固定で、同一セッションからの重複を防止する。

    Attributes:
        post: リアクション対象のレス（削除時はカスケード削除）
        user_session: リアクションしたセッション（削除時はNULLに設定）
        reaction_type: リアクションの種類（like, useful, funnyなど）
        created_at: リアクション日時
    """

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
        # NOTE: 同一セッションから同一レスへの同じリアクションを防止
        unique_together = [["post", "user_session", "reaction_type"]]
        indexes = [
            models.Index(fields=["post", "reaction_type"]),
        ]

    def __str__(self) -> str:
        """リアクションの文字列表現を返す.

        Returns:
            リアクション種類とレス番号の組み合わせ
        """
        return f"{self.reaction_type} on Post #{self.post.post_number}"
