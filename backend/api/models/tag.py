"""掲示板のタグモデル.

スレッドに付与するタグを管理する。
ユーザーが自由に作成可能で、検索・フィルタリングに使用される。
"""

from django.db import models


class Tag(models.Model):
    """スレッドのタグを表すモデル.

    スレッドに付与するタグ情報を保持する。
    トレンドタグの抽出や、タグによる絞り込み検索に使用される。

    Attributes:
        name: タグ名（例: Python, React, 初心者向け）
        slug: URL用のスラッグ（例: python, react, beginner）
        created_at: 作成日時
    """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "board_tag"
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        """タグの文字列表現を返す.

        Returns:
            タグ名
        """
        return self.name
