"""Views for thread endpoints."""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Thread
from api.v1.threads.serializers import (
    ThreadCreateSerializer,
    ThreadDetailSerializer,
    ThreadListSerializer,
)


class ThreadViewSet(viewsets.ModelViewSet):
    """ViewSet for thread operations."""

    queryset = (
        Thread.objects.all()
        .select_related("category", "author_session")
        .prefetch_related("tags")
    )

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "list":
            return ThreadListSerializer
        if self.action == "create":
            return ThreadCreateSerializer
        return ThreadDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a thread and increment view count."""
        thread = self.get_object()
        thread.view_count += 1
        thread.save(update_fields=["view_count"])
        serializer = self.get_serializer(thread)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def trending(self, request):
        """Get trending threads sorted by momentum."""
        threads = Thread.objects.all().order_by("-momentum")[:20]
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """Get recently active threads."""
        threads = Thread.objects.all().order_by("-last_post_at")[:20]
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def pin(self, request, pk=None):
        """Pin/unpin a thread."""
        thread = self.get_object()
        thread.is_pinned = not thread.is_pinned
        thread.save(update_fields=["is_pinned"])
        serializer = self.get_serializer(thread)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def lock(self, request, pk=None):
        """Lock/unlock a thread."""
        thread = self.get_object()
        thread.is_locked = not thread.is_locked
        thread.save(update_fields=["is_locked"])
        serializer = self.get_serializer(thread)
        return Response(serializer.data)
