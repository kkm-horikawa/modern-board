"""URL routing for API v1."""

from django.urls import include, path

urlpatterns = [
    path("threads/", include("api.v1.threads.urls")),
    path("posts/", include("api.v1.posts.urls")),
    path("categories/", include("api.v1.categories.urls")),
    path("tags/", include("api.v1.tags.urls")),
    path("stats/", include("api.v1.stats.urls")),
]
