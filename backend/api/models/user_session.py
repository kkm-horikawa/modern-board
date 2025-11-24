"""匿名ユーザーセッションモデル.

ユーザー登録なしで投稿できる匿名掲示板のため、
セッションベースでユーザーを識別・追跡する。
"""

import uuid

from django.db import models


class UserSession(models.Model):
    """匿名ユーザーのセッション情報を表すモデル.

    ユーザー登録なしでの投稿を実現するため、セッションIDでユーザーを識別する。
    投稿数やポイントなどの統計情報を保持し、フロントエンドで表示する。

    Attributes:
        session_id: セッションを一意に識別するUUID
        temporary_name: 自動生成された一時的な表示名（例: ID:abc123）
        post_count: レス投稿数
        thread_count: 作成したスレッド数
        total_points: 獲得ポイント総数（フロントエンド表示用）
        level: レベル（ポイントから計算）
        created_at: セッション作成日時
        last_activity_at: 最終アクティビティ日時
    """

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

    def __str__(self) -> str:
        """セッションの文字列表現を返す.

        Returns:
            一時的な表示名
        """
        return self.temporary_name
