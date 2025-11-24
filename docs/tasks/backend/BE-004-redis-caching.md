# BE-004: Redisキャッシュの導入

## 概要
パフォーマンス向上のため、Redisキャッシュを導入し、頻繁にアクセスされるデータをキャッシュする。

## 優先度
**Low** - 初期開発では必須ではないが、スケーリングに重要

## 難易度
**Medium**

## 前提条件
- [x] Django設定が完了している
- [ ] Redisサーバーが利用可能（Docker環境推奨）
- [ ] 基本的なAPI実装が完了している

## 実装内容

### 1. Redis環境のセットアップ
- [ ] `docker-compose.yml`にRedisサービスを追加
- [ ] `django-redis`パッケージのインストール
- [ ] `redis-py`のインストール
- [ ] 開発環境と本番環境での接続設定

### 2. Djangoキャッシュ設定
- [ ] `settings.py`でRedisをデフォルトキャッシュバックエンドに設定
- [ ] セッションストレージをRedisに移行（オプション）
- [ ] キャッシュキーのプレフィックス設定
- [ ] タイムアウト設定

### 3. ビューレベルキャッシュ
- [ ] 一覧APIのキャッシュ（カテゴリ、タグ、スレッド）
- [ ] 統計APIのキャッシュ（board_stats, trending_threads等）
- [ ] `@cache_page`デコレータの活用
- [ ] 条件付きキャッシュ（認証状態による切り替え）

### 4. クエリセットキャッシュ
- [ ] 頻繁に使われるクエリのキャッシュ
- [ ] `select_related`/`prefetch_related`の最適化
- [ ] カスタムキャッシュ関数の作成

### 5. キャッシュ無効化戦略
- [ ] モデルシグナルによる自動無効化
- [ ] 手動無効化のユーティリティ関数
- [ ] タグベースキャッシュ無効化
- [ ] パターンマッチングでの一括削除

### 6. モニタリング
- [ ] キャッシュヒット率の計測
- [ ] Redis接続プールの監視
- [ ] メモリ使用量の監視
- [ ] キャッシュキーの一覧表示機能（開発用）

### 7. テスト
- [ ] キャッシュが正しく機能することの確認
- [ ] 無効化が正しく動作することの確認
- [ ] Redisダウン時のフォールバック動作テスト

## 受け入れ基準
- [ ] Redisが正常に動作している
- [ ] キャッシュが有効な場合、レスポンス時間が改善される
- [ ] データ更新時にキャッシュが適切に無効化される
- [ ] Redis接続エラー時もアプリケーションが動作する
- [ ] キャッシュヒット率が50%以上（目標）

## Docker Compose設定例
```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  redis_data:
```

## Django設定例
```python
# settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "modern_board",
        "TIMEOUT": 300,  # 5 minutes default
    }
}
```

## 関連タスク
- BE-003: スパム対策・レート制限（Redisを活用）
- BE-005: APIパフォーマンステスト
- INF-001: Docker環境の改善
- INF-002: 本番環境Redis設定

## 参考
- django-redis: https://github.com/jazzband/django-redis
- Django Caching: https://docs.djangoproject.com/en/5.2/topics/cache/
- Redis Best Practices: https://redis.io/docs/manual/patterns/
