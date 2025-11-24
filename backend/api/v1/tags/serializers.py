"""タグエンドポイント用シリアライザー.

タグの一覧取得、詳細表示、作成、更新のためのシリアライザーを提供する。
"""

from rest_framework import serializers

from api.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """タグモデル用シリアライザー.

    タグの全フィールドとこのタグが付けられたスレッド数を含む詳細な情報を提供する。
    タグの作成、更新、詳細表示に使用する。

    Attributes:
        thread_count: このタグが付けられているスレッド数（読み取り専用）
    """

    thread_count = serializers.IntegerField(
        source="threads.count",
        read_only=True,
        help_text="Number of threads with this tag",
    )

    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "thread_count", "created_at"]
        read_only_fields = ["id", "created_at", "thread_count"]


class TagListSerializer(serializers.ModelSerializer):
    """タグ一覧用の軽量シリアライザー.

    タグ一覧表示やスレッドに関連付けられたタグ表示に使用する。
    パフォーマンスを考慮し、必須情報（id, name, slug）のみを含む。
    """

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
        read_only_fields = ["id"]
