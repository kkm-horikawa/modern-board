"""URL routing for stats endpoints."""

from django.urls import path

from api.v1.stats.views import activity_feed, board_stats, top_users, trending_threads

urlpatterns = [
    path("board/", board_stats, name="board-stats"),
    path("trending/", trending_threads, name="trending-threads"),
    path("top-users/", top_users, name="top-users"),
    path("activity/", activity_feed, name="activity-feed"),
]
