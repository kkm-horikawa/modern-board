"""Views for post endpoints."""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Post, Reaction
from api.v1.posts.serializers import (
    PostCreateSerializer,
    PostSerializer,
    ReactionSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for post operations."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "create":
            return PostCreateSerializer
        return PostSerializer

    def create(self, request, *args, **kwargs):
        """Create a new post."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get or create user session (simplified for now)
        # In full implementation, this would use middleware or service layer
        thread = serializer.validated_data["thread"]

        # Calculate next post number
        last_post = Post.objects.filter(thread=thread).order_by("-post_number").first()
        next_number = (last_post.post_number + 1) if last_post else 1

        post = Post.objects.create(
            thread=thread,
            content=serializer.validated_data["content"],
            reply_to=serializer.validated_data.get("reply_to"),
            post_number=next_number,
            is_op=(next_number == 1),
        )

        # Update thread stats
        thread.post_count = Post.objects.filter(thread=thread).count()
        thread.last_post_at = post.created_at
        thread.save()

        output_serializer = PostSerializer(post)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def react(self, request, pk=None):
        """Add a reaction to a post."""
        post = self.get_object()
        reaction_type = request.data.get("reaction_type")

        if not reaction_type:
            return Response(
                {"error": "reaction_type is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # For now, allow duplicate reactions (no user session tracking)
        reaction = Reaction.objects.create(post=post, reaction_type=reaction_type)

        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
