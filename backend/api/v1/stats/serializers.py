"""統計情報エンドポイント用シリアライザー.

掲示板全体の統計情報、トレンドスレッド、トップユーザー、
アクティビティフィードなどの集計データを提供する。
"""

from rest_framework import serializers


class BoardStatsSerializer(serializers.Serializer):
    """掲示板全体の統計情報シリアライザー.

    掲示板全体のサマリー統計を提供する。

    Attributes:
        total_threads: 総スレッド数
        total_posts: 総投稿数
        total_users: 総ユーザー（セッション）数
        active_threads_24h: 過去24時間にアクティブなスレッド数
    """

    total_threads = serializers.IntegerField()
    total_posts = serializers.IntegerField()
    total_users = serializers.IntegerField()
    active_threads_24h = serializers.IntegerField()


class TrendingThreadSerializer(serializers.Serializer):
    """トレンドスレッド用シリアライザー.

    勢いがあるスレッドの情報を提供する。
    勢いスコア（momentum）でソートされる。

    Attributes:
        id: スレッドID
        title: スレッドタイトル
        momentum: 勢いスコア（レス/時）
        post_count: 投稿数
        view_count: 閲覧数
    """

    id = serializers.IntegerField()
    title = serializers.CharField()
    momentum = serializers.FloatField()
    post_count = serializers.IntegerField()
    view_count = serializers.IntegerField()


class TopUserSerializer(serializers.Serializer):
    """トップユーザー（MVP）用シリアライザー.

    ポイント獲得上位のユーザー情報を提供する。

    Attributes:
        temporary_name: ユーザーの一時名
        total_points: 総獲得ポイント
        level: ユーザーレベル
        post_count: 投稿数
        thread_count: スレッド作成数
    """

    temporary_name = serializers.CharField()
    total_points = serializers.IntegerField()
    level = serializers.IntegerField()
    post_count = serializers.IntegerField()
    thread_count = serializers.IntegerField()


class ActivityFeedSerializer(serializers.Serializer):
    """アクティビティフィード用シリアライザー.

    最近のアクティビティ（スレッド作成、投稿、リアクション）を
    時系列で提供する。

    Attributes:
        id: アクティビティID
        type: アクティビティタイプ（'thread', 'post', 'reaction'）
        thread_id: 関連スレッドID（任意）
        thread_title: 関連スレッドタイトル（任意）
        post_number: 投稿番号（任意）
        content_preview: 投稿内容のプレビュー（任意）
        author_name: 作成者名（任意）
        created_at: 作成日時
    """

    id = serializers.IntegerField()
    type = serializers.CharField()  # 'thread', 'post', 'reaction'
    thread_id = serializers.IntegerField(required=False, allow_null=True)
    thread_title = serializers.CharField(required=False, allow_null=True)
    post_number = serializers.IntegerField(required=False, allow_null=True)
    content_preview = serializers.CharField(required=False, allow_null=True)
    author_name = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField()
