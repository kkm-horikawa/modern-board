"""Serializers for post endpoints."""

from rest_framework import serializers

from api.models import Post, Reaction


class ReactionCountSerializer(serializers.Serializer):
    """Serializer for reaction counts."""

    reaction_type = serializers.CharField()
    count = serializers.IntegerField()


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model."""

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
        """Get aggregated reaction counts for this post."""
        from django.db.models import Count

        counts = (
            Reaction.objects.filter(post=obj)
            .values("reaction_type")
            .annotate(count=Count("id"))
        )
        return ReactionCountSerializer(counts, many=True).data


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts."""

    class Meta:
        model = Post
        fields = ["thread", "content", "reply_to"]


class ReactionSerializer(serializers.ModelSerializer):
    """Serializer for Reaction model."""

    class Meta:
        model = Reaction
        fields = ["id", "post", "reaction_type", "created_at"]
        read_only_fields = ["id", "created_at"]
