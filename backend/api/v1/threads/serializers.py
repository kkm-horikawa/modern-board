"""Serializers for thread endpoints."""

from rest_framework import serializers

from api.models import Thread
from api.v1.posts.serializers import PostSerializer
from api.v1.tags.serializers import TagListSerializer


class ThreadListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for thread lists."""

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
    """Detailed serializer for thread with posts."""

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
    """Serializer for creating threads."""

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
        """Create thread with initial post."""
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
