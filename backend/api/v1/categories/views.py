"""Views for category endpoints."""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Category
from api.v1.categories.serializers import CategoryListSerializer, CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for category operations."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "list":
            return CategoryListSerializer
        return CategorySerializer

    @action(detail=True, methods=["get"])
    def threads(self, request, pk=None):
        """Get threads for a specific category."""
        category = self.get_object()
        from api.v1.threads.serializers import ThreadListSerializer

        threads = category.threads.all()
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)
