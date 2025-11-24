"""スレッドエンドポイント用ビュー.

スレッドのCRUD操作、トレンド表示、ピン留め、ロックなどの
全機能を提供する。
"""

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
    """スレッド操作用ViewSet.

    スレッドのCRUD操作と各種アクション（トレンド、ピン留め、ロックなど）を提供する。
    パフォーマンスを考慮し、select_relatedとprefetch_relatedで関連データを最適化。

    Attributes:
        queryset: スレッドのQuerySet（関連データを最適化済み）
    """

    queryset = (
        Thread.objects.all()
        .select_related("category", "author_session")
        .prefetch_related("tags")
    )

    def get_serializer_class(self):
        """アクションに応じた適切なシリアライザーを返す.

        Returns:
            一覧表示: ThreadListSerializer
            作成: ThreadCreateSerializer
            その他: ThreadDetailSerializer
        """
        if self.action == "list":
            return ThreadListSerializer
        if self.action == "create":
            return ThreadCreateSerializer
        return ThreadDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        """スレッドを取得し、閲覧数をインクリメントする.

        Args:
            request: HTTPリクエスト
            *args: 可変長引数
            **kwargs: キーワード引数

        Returns:
            スレッドの詳細データ
        """
        thread = self.get_object()
        thread.view_count += 1
        thread.save(update_fields=["view_count"])
        serializer = self.get_serializer(thread)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def trending(self, request):
        """勢いスコアでソートされたトレンドスレッドを取得する.

        Args:
            request: HTTPリクエスト

        Returns:
            勢いスコア降順で上位20件のスレッド
        """
        threads = Thread.objects.all().order_by("-momentum")[:20]
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """最近アクティブなスレッドを取得する.

        Args:
            request: HTTPリクエスト

        Returns:
            最終投稿日時降順で上位20件のスレッド
        """
        threads = Thread.objects.all().order_by("-last_post_at")[:20]
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def pin(self, request, pk=None):
        """スレッドをピン留め/ピン留め解除する.

        Args:
            request: HTTPリクエスト
            pk: スレッドID

        Returns:
            更新されたスレッドデータ
        """
        thread = self.get_object()
        thread.is_pinned = not thread.is_pinned
        thread.save(update_fields=["is_pinned"])
        serializer = self.get_serializer(thread)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def lock(self, request, pk=None):
        """スレッドをロック/ロック解除する.

        Args:
            request: HTTPリクエスト
            pk: スレッドID

        Returns:
            更新されたスレッドデータ
        """
        thread = self.get_object()
        thread.is_locked = not thread.is_locked
        thread.save(update_fields=["is_locked"])
        serializer = self.get_serializer(thread)
        return Response(serializer.data)
