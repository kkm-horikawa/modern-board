"""スレッドエンドポイント用シリアライザー.

スレッドの一覧取得、詳細表示、作成、更新のためのシリアライザーを提供する。
"""

from rest_framework import serializers

from api.models import Thread
from api.v1.posts.serializers import PostSerializer
from api.v1.tags.serializers import TagListSerializer


class ThreadListSerializer(serializers.ModelSerializer):
    """スレッド一覧用の軽量シリアライザー.

    スレッド一覧表示に必要な情報を提供する。
    パフォーマンスを考慮し、投稿内容は含まず、メタデータのみを返す。

    Attributes:
        category_name: 所属カテゴリ名（読み取り専用）
        author_name: 作成者の一時名（読み取り専用、NULL許可）
        tags: 関連付けられたタグのリスト（読み取り専用）
    """

    category_name = serializers.CharField(source="category.name", read_only=True)
    author_name = serializers.CharField(
        source="author_session.temporary_name", read_only=True, allow_null=True
    )
    tags = TagListSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = [
            "id",
            "title",
            "category_name",
            "tags",
            "author_name",
            "post_count",
            "view_count",
            "momentum",
            "is_pinned",
            "is_locked",
            "created_at",
            "last_post_at",
        ]
        read_only_fields = [
            "id",
            "post_count",
            "view_count",
            "momentum",
            "created_at",
            "last_post_at",
        ]


class ThreadDetailSerializer(serializers.ModelSerializer):
    """スレッド詳細用の完全なシリアライザー.

    スレッドの詳細情報と全ての投稿を含む完全なデータを提供する。
    スレッド詳細画面での表示に使用する。

    Attributes:
        category_name: 所属カテゴリ名（読み取り専用）
        author_name: 作成者の一時名（読み取り専用、NULL許可）
        tags: 関連付けられたタグのリスト（読み取り専用）
        posts: スレッド内の全投稿のリスト（読み取り専用）
    """

    category_name = serializers.CharField(source="category.name", read_only=True)
    author_name = serializers.CharField(
        source="author_session.temporary_name", read_only=True, allow_null=True
    )
    tags = TagListSerializer(many=True, read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = [
            "id",
            "title",
            "category",
            "category_name",
            "tags",
            "author_name",
            "post_count",
            "view_count",
            "momentum",
            "is_pinned",
            "is_locked",
            "posts",
            "created_at",
            "updated_at",
            "last_post_at",
        ]
        read_only_fields = [
            "id",
            "post_count",
            "view_count",
            "momentum",
            "created_at",
            "updated_at",
            "last_post_at",
        ]


class ThreadCreateSerializer(serializers.ModelSerializer):
    """スレッド作成用のシリアライザー.

    新しいスレッドと最初の投稿（OP）を作成する。
    スレッド作成時には必ず最初の投稿を含める必要がある。

    Attributes:
        tag_ids: スレッドに関連付けるタグのIDリスト（書き込み専用、任意）
        initial_post_content: 最初の投稿の内容（書き込み専用、必須）
    """

    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    initial_post_content = serializers.CharField(
        write_only=True, help_text="Content for the first post"
    )

    class Meta:
        model = Thread
        fields = ["title", "category", "tag_ids", "initial_post_content"]

    def create(self, validated_data):
        """スレッドと最初の投稿を作成する.

        Args:
            validated_data: バリデーション済みのデータ辞書

        Returns:
            作成されたThreadインスタンス

        Note:
            最初の投稿（post_number=1, is_op=True）を自動的に作成する。
            タグが指定されている場合は、スレッドに関連付ける。
        """
        tag_ids = validated_data.pop("tag_ids", [])
        initial_post_content = validated_data.pop("initial_post_content")

        thread = Thread.objects.create(**validated_data)

        if tag_ids:
            thread.tags.set(tag_ids)

        # Create initial post (handled by service layer in full implementation)
        from api.models import Post

        Post.objects.create(
            thread=thread,
            content=initial_post_content,
            post_number=1,
            is_op=True,
            author_session=validated_data.get("author_session"),
        )

        thread.post_count = 1
        thread.last_post_at = thread.created_at
        thread.save()

        return thread
