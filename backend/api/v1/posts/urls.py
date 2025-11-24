"""URL routing for posts endpoints."""

from rest_framework.routers import DefaultRouter

from api.v1.posts.views import PostViewSet

router = DefaultRouter()
router.register(r"", PostViewSet, basename="post")

urlpatterns = router.urls
