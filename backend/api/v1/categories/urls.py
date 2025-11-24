"""URL routing for categories endpoints."""

from rest_framework.routers import DefaultRouter

from api.v1.categories.views import CategoryViewSet

router = DefaultRouter()
router.register(r"", CategoryViewSet, basename="category")

urlpatterns = router.urls
