"""Serializers for tag endpoints."""

from rest_framework import serializers

from api.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""

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
    """Lightweight serializer for tag lists."""

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
        read_only_fields = ["id"]
