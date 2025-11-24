"""カテゴリエンドポイント用ビュー.

カテゴリの一覧取得、詳細表示、およびカテゴリ内のスレッド一覧を提供する。
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Category
from api.v1.categories.serializers import CategoryListSerializer, CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """カテゴリ操作用ViewSet.

    カテゴリの読み取り専用エンドポイントを提供する。
    一覧表示、詳細表示、およびカテゴリに属するスレッドの取得が可能。

    Attributes:
        queryset: カテゴリの全件QuerySet
        serializer_class: デフォルトのシリアライザー
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        """アクションに応じた適切なシリアライザーを返す.

        Returns:
            一覧表示: CategoryListSerializer
            その他: CategorySerializer
        """
        if self.action == "list":
            return CategoryListSerializer
        return CategorySerializer

    @action(detail=True, methods=["get"])
    def threads(self, request, pk=None):
        """特定カテゴリのスレッド一覧を取得する.

        Args:
            request: HTTPリクエスト
            pk: カテゴリID

        Returns:
            カテゴリに属するスレッドのリスト
        """
        category = self.get_object()
        from api.v1.threads.serializers import ThreadListSerializer

        threads = category.threads.all()
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)
