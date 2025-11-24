"""投稿エンドポイント用ビュー.

投稿（レス）のCRUD操作とリアクション機能を提供する。
"""

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
    """投稿操作用ViewSet.

    投稿のCRUD操作とリアクション追加機能を提供する。
    投稿番号は自動的に採番され、スレッド統計も更新される。

    Attributes:
        queryset: 投稿の全件QuerySet
        serializer_class: デフォルトのシリアライザー
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        """アクションに応じた適切なシリアライザーを返す.

        Returns:
            作成: PostCreateSerializer
            その他: PostSerializer
        """
        if self.action == "create":
            return PostCreateSerializer
        return PostSerializer

    def create(self, request, *args, **kwargs):
        """新しい投稿を作成する.

        Args:
            request: HTTPリクエスト
            *args: 可変長引数
            **kwargs: キーワード引数

        Returns:
            作成された投稿データ

        Note:
            投稿番号は自動的に採番される。
            スレッドの投稿数と最終投稿日時も更新される。
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # NOTE: ユーザーセッションの取得/作成は簡略化
        # 完全な実装では、ミドルウェアまたはサービス層で処理
        thread = serializer.validated_data["thread"]

        # NOTE: 次の投稿番号を計算
        last_post = Post.objects.filter(thread=thread).order_by("-post_number").first()
        next_number = (last_post.post_number + 1) if last_post else 1

        post = Post.objects.create(
            thread=thread,
            content=serializer.validated_data["content"],
            reply_to=serializer.validated_data.get("reply_to"),
            post_number=next_number,
            is_op=(next_number == 1),
        )

        # NOTE: スレッド統計を更新
        thread.post_count = Post.objects.filter(thread=thread).count()
        thread.last_post_at = post.created_at
        thread.save()

        output_serializer = PostSerializer(post)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def react(self, request, pk=None):
        """投稿にリアクションを追加する.

        Args:
            request: HTTPリクエスト
            pk: 投稿ID

        Returns:
            作成されたリアクションデータ

        Note:
            現在の実装では重複リアクションを許可。
            完全な実装では、ユーザーセッションによる重複防止を行う。
        """
        post = self.get_object()
        reaction_type = request.data.get("reaction_type")

        if not reaction_type:
            return Response(
                {"error": "reaction_type is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # NOTE: 現時点では重複リアクションを許可（ユーザーセッション未追跡）
        reaction = Reaction.objects.create(post=post, reaction_type=reaction_type)

        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
