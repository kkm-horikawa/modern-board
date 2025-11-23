"""Serializers for category endpoints."""

from rest_framework import serializers

from api.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

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
    """Lightweight serializer for category lists."""

    thread_count = serializers.IntegerField(
        source="threads.count",
        read_only=True,
        help_text="Number of threads in this category",
    )

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "thread_count"]
        read_only_fields = ["id", "thread_count"]
