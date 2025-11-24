"""タグエンドポイント用ビュー.

タグの一覧取得、詳細表示、およびタグが付けられたスレッド一覧を提供する。
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Tag
from api.v1.tags.serializers import TagListSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """タグ操作用ViewSet.

    タグの読み取り専用エンドポイントを提供する。
    一覧表示、詳細表示、およびタグが付けられたスレッドの取得が可能。

    Attributes:
        queryset: タグの全件QuerySet
        serializer_class: デフォルトのシリアライザー
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_serializer_class(self):
        """アクションに応じた適切なシリアライザーを返す.

        Returns:
            一覧表示: TagListSerializer
            その他: TagSerializer
        """
        if self.action == "list":
            return TagListSerializer
        return TagSerializer

    @action(detail=True, methods=["get"])
    def threads(self, request, pk=None):
        """特定タグが付けられたスレッド一覧を取得する.

        Args:
            request: HTTPリクエスト
            pk: タグID

        Returns:
            タグが付けられたスレッドのリスト
        """
        tag = self.get_object()
        from api.v1.threads.serializers import ThreadListSerializer

        threads = tag.threads.all()
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)
