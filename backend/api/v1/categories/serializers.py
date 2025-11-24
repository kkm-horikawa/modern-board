"""カテゴリエンドポイント用シリアライザー.

カテゴリの一覧取得、詳細表示、作成、更新のためのシリアライザーを提供する。
"""

from rest_framework import serializers

from api.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """カテゴリモデル用シリアライザー.

    カテゴリの全フィールドとスレッド数を含む詳細な情報を提供する。
    カテゴリの作成、更新、詳細表示に使用する。

    Attributes:
        thread_count: カテゴリに属するスレッド数（読み取り専用）
    """

    thread_count = serializers.IntegerField(
        source="threads.count",
        read_only=True,
        help_text="Number of threads in this category",
    )

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "display_order",
            "thread_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "thread_count"]


class CategoryListSerializer(serializers.ModelSerializer):
    """カテゴリ一覧用の軽量シリアライザー.

    カテゴリ一覧表示に必要最小限のフィールドのみを提供する。
    パフォーマンスを考慮し、必須情報（id, name, slug, thread_count）のみを含む。

    Attributes:
        thread_count: カテゴリに属するスレッド数（読み取り専用）
    """

    thread_count = serializers.IntegerField(
        source="threads.count",
        read_only=True,
        help_text="Number of threads in this category",
    )

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "thread_count"]
        read_only_fields = ["id", "thread_count"]
