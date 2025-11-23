"""Serializers for stats endpoints."""

from rest_framework import serializers


class BoardStatsSerializer(serializers.Serializer):
    """Serializer for overall board statistics."""

    total_threads = serializers.IntegerField()
    total_posts = serializers.IntegerField()
    total_users = serializers.IntegerField()
    active_threads_24h = serializers.IntegerField()


class TrendingThreadSerializer(serializers.Serializer):
    """Serializer for trending threads."""

    id = serializers.IntegerField()
    title = serializers.CharField()
    momentum = serializers.FloatField()
    post_count = serializers.IntegerField()
    view_count = serializers.IntegerField()


class TopUserSerializer(serializers.Serializer):
    """Serializer for top users/MVPs."""

    temporary_name = serializers.CharField()
    total_points = serializers.IntegerField()
    level = serializers.IntegerField()
    post_count = serializers.IntegerField()
    thread_count = serializers.IntegerField()


class ActivityFeedSerializer(serializers.Serializer):
    """Serializer for activity feed."""

    id = serializers.IntegerField()
    type = serializers.CharField()  # 'thread', 'post', 'reaction'
    thread_id = serializers.IntegerField(required=False, allow_null=True)
    thread_title = serializers.CharField(required=False, allow_null=True)
    post_number = serializers.IntegerField(required=False, allow_null=True)
    content_preview = serializers.CharField(required=False, allow_null=True)
    author_name = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField()
