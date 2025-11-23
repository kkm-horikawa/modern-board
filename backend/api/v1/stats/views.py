"""Views for stats endpoints."""

from datetime import timedelta

from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Post, Thread, UserSession
from api.v1.stats.serializers import (
    ActivityFeedSerializer,
    BoardStatsSerializer,
    TopUserSerializer,
    TrendingThreadSerializer,
)


@api_view(["GET"])
def board_stats(request):
    """Get overall board statistics."""
    stats = {
        "total_threads": Thread.objects.count(),
        "total_posts": Post.objects.count(),
        "total_users": UserSession.objects.count(),
        "active_threads_24h": Thread.objects.filter(
            last_post_at__gte=timezone.now() - timedelta(hours=24)
        ).count(),
    }
    serializer = BoardStatsSerializer(stats)
    return Response(serializer.data)


@api_view(["GET"])
def trending_threads(request):
    """Get trending threads by momentum."""
    threads = (
        Thread.objects.all()
        .order_by("-momentum")[:10]
        .values("id", "title", "momentum", "post_count", "view_count")
    )
    serializer = TrendingThreadSerializer(threads, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def top_users(request):
    """Get top users/MVPs by points."""
    users = UserSession.objects.all().order_by("-total_points")[:10]
    serializer = TopUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def activity_feed(request):
    """Get recent activity feed."""
    # Get recent posts with thread info
    recent_posts = (
        Post.objects.all()
        .select_related("thread", "author_session")
        .order_by("-created_at")[:20]
    )

    activities = []
    for post in recent_posts:
        activities.append(
            {
                "id": post.id,
                "type": "post",
                "thread_id": post.thread.id,
                "thread_title": post.thread.title,
                "post_number": post.post_number,
                "content_preview": post.content[:100]
                if len(post.content) > 100
                else post.content,
                "author_name": post.author_session.temporary_name
                if post.author_session
                else "匿名",
                "created_at": post.created_at,
            }
        )

    serializer = ActivityFeedSerializer(activities, many=True)
    return Response(serializer.data)
