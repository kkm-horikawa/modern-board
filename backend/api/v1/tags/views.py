"""Views for tag endpoints."""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Tag
from api.v1.tags.serializers import TagListSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for tag operations."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "list":
            return TagListSerializer
        return TagSerializer

    @action(detail=True, methods=["get"])
    def threads(self, request, pk=None):
        """Get threads with a specific tag."""
        tag = self.get_object()
        from api.v1.threads.serializers import ThreadListSerializer

        threads = tag.threads.all()
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)
