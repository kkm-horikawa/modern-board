"""URL routing for tags endpoints."""

from rest_framework.routers import DefaultRouter

from api.v1.tags.views import TagViewSet

router = DefaultRouter()
router.register(r"", TagViewSet, basename="tag")

urlpatterns = router.urls
