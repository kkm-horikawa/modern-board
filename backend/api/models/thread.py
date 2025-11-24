"""掲示板のスレッドモデル.

掲示板のメインコンテンツとなるスレッド（ディスカッション）を管理する。
勢いスコアの計算やピン留め、ロック機能などを提供する。
"""

from django.db import models


class Thread(models.Model):
    """掲示板スレッドを表すモデル.

    ディスカッションの場となるスレッド情報を保持する。
    カテゴリ分類、タグ付け、勢いスコア計算、ピン留めなどの機能を持つ。

    Attributes:
        title: スレッドタイトル（最大200文字）
        category: 所属カテゴリ（削除時はカスケード削除）
        tags: 関連付けられたタグ（多対多）
        author_session: 作成者のセッション（削除時はNULLに設定）
        post_count: レス数（投稿のたびに更新）
        view_count: 閲覧数（詳細画面表示のたびにインクリメント）
        momentum: 勢いスコア（直近の投稿頻度から計算）
        is_pinned: ピン留めフラグ（一覧の最上部に固定）
        is_locked: ロックフラグ（新規投稿を禁止）
        created_at: 作成日時
        updated_at: 更新日時
        last_post_at: 最終投稿日時（ソート用）
    """

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

    def __str__(self) -> str:
        """スレッドの文字列表現を返す.

        Returns:
            スレッドタイトル
        """
        return self.title
