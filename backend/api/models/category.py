"""掲示板のカテゴリモデル.

スレッドを分類するためのカテゴリを管理する。
固定カテゴリ（プログラミング、雑談、相談など）を想定。
"""

from django.db import models


class Category(models.Model):
    """スレッドのカテゴリを表すモデル.

    スレッドを分類するためのカテゴリ情報を保持する。
    表示順序を指定でき、一覧画面でソート順として使用される。

    Attributes:
        name: カテゴリ名（例: プログラミング、雑談）
        slug: URL用のスラッグ（例: programming, chat）
        description: カテゴリの説明文
        display_order: 表示順序（昇順）
        created_at: 作成日時
        updated_at: 更新日時
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")
    display_order = models.IntegerField(
        default=0, help_text="Display order on the board"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "board_category"
        ordering = ["display_order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        """カテゴリの文字列表現を返す.

        Returns:
            カテゴリ名
        """
        return self.name
