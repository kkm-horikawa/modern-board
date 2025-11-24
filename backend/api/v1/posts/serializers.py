"""投稿エンドポイント用シリアライザー.

投稿（レス）とリアクションの一覧取得、詳細表示、作成、更新のための
シリアライザーを提供する。
"""

from rest_framework import serializers

from api.models import Post, Reaction


class ReactionCountSerializer(serializers.Serializer):
    """リアクション集計用シリアライザー.

    投稿に対するリアクションをタイプ別に集計した結果を表現する。

    Attributes:
        reaction_type: リアクションタイプ（like, useful, funnyなど）
        count: 該当タイプのリアクション数
    """

    reaction_type = serializers.CharField()
    count = serializers.IntegerField()


class PostSerializer(serializers.ModelSerializer):
    """投稿モデル用シリアライザー.

    投稿の詳細情報とリアクション集計、返信数を含む完全なデータを提供する。
    投稿の作成、更新、詳細表示に使用する。

    Attributes:
        author_name: 投稿者の一時名（読み取り専用、NULL許可）
        reaction_counts: リアクション種類別の集計（メソッドフィールド）
        reply_count: この投稿への返信数（読み取り専用）
    """

    author_name = serializers.CharField(
        source="author_session.temporary_name", read_only=True, allow_null=True
    )
    reaction_counts = serializers.SerializerMethodField()
    reply_count = serializers.IntegerField(source="replies.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "thread",
            "content",
            "post_number",
            "reply_to",
            "is_op",
            "author_name",
            "reaction_counts",
            "reply_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "post_number",
            "is_op",
            "author_name",
            "reaction_counts",
            "reply_count",
            "created_at",
            "updated_at",
        ]

    def get_reaction_counts(self, obj):
        """投稿のリアクション集計を取得する.

        Args:
            obj: 対象のPostインスタンス

        Returns:
            リアクションタイプ別の集計データのリスト
        """
        from django.db.models import Count

        counts = (
            Reaction.objects.filter(post=obj)
            .values("reaction_type")
            .annotate(count=Count("id"))
        )
        return ReactionCountSerializer(counts, many=True).data


class PostCreateSerializer(serializers.ModelSerializer):
    """投稿作成用のシリアライザー.

    新しい投稿をスレッドに追加する。
    投稿番号は自動的に採番される。
    """

    class Meta:
        model = Post
        fields = ["thread", "content", "reply_to"]


class ReactionSerializer(serializers.ModelSerializer):
    """リアクションモデル用シリアライザー.

    投稿に対するリアクション（いいね、面白いなど）を管理する。
    同一セッションからの重複リアクションは防止される。
    """

    class Meta:
        model = Reaction
        fields = ["id", "post", "reaction_type", "created_at"]
        read_only_fields = ["id", "created_at"]
