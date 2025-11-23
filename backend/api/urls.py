"""URL routing for API endpoints."""

from rest_framework.routers import DefaultRouter

# Create a router for ViewSets
router = DefaultRouter()

# Register ViewSets here
# router.register(r'resource', ResourceViewSet)

urlpatterns = router.urls
