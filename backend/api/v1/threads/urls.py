"""URL routing for threads endpoints."""

from rest_framework.routers import DefaultRouter

from api.v1.threads.views import ThreadViewSet

router = DefaultRouter()
router.register(r"", ThreadViewSet, basename="thread")

urlpatterns = router.urls
