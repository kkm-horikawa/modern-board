# BE-003: スパム対策・レート制限の実装

## 概要
掲示板システムにおけるスパム投稿や連投を防止するため、レート制限とスパム検出機能を実装する。

## 優先度
**Medium** - 公開後すぐに必要だが、初期開発には必須ではない

## 難易度
**Medium**

## 前提条件
- [x] 投稿APIが実装済み
- [x] UserSessionモデルが実装済み
- [ ] BE-002: 認証・認可システムが完成している

## 実装内容

### 1. DRF Throttling（基本的なレート制限）
- [ ] `settings.py`にthrottling設定を追加
- [ ] AnonRateThrottle: 匿名ユーザー向けレート制限
- [ ] UserRateThrottle: セッションユーザー向けレート制限
- [ ] ViewSet単位でのthrottle_classesの設定
- [ ] カスタムthrottleクラスの作成（必要に応じて）

### 2. IPベースレート制限
- [ ] IPアドレス取得のユーティリティ関数（Proxy対応）
- [ ] 同一IPからの連続投稿を制限（例: 10秒に1回まで）
- [ ] スレッド作成の制限（例: 1時間に3スレッドまで）
- [ ] Redis等を使った分散環境対応（オプション）

### 3. スパム検出機能
- [ ] 重複投稿の検出（同一内容の連投防止）
- [ ] 短時間での大量投稿の検出
- [ ] NGワードフィルタ（設定可能）
- [ ] URLスパムの検出（過剰なURL含有投稿）
- [ ] 文字数異常の検出（極端に長い/短い投稿）

### 4. キャッシュ機構（Redis推奨）
- [ ] django-redis のセットアップ
- [ ] レート制限カウンターのキャッシュ化
- [ ] スパム検出用のブルームフィルタ（オプション）

### 5. 管理機能
- [ ] ブロックリストの管理（IP、セッション）
- [ ] レート制限の動的変更機能
- [ ] スパム報告機能（ユーザーからの通報）
- [ ] 自動ブロックの解除機能

### 6. テスト
- [ ] レート制限超過時のエラーレスポンステスト
- [ ] スパム検出ロジックのテスト
- [ ] キャッシュ動作のテスト
- [ ] 正常な投稿が制限されないことの確認

## 受け入れ基準
- [ ] レート制限が正しく動作する（429 Too Many Requests）
- [ ] スパム投稿が検出され、拒否される
- [ ] 正常な投稿は制限されない
- [ ] レート制限情報がレスポンスヘッダーに含まれる
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
- [ ] 管理画面からブロックリストを管理できる
- [ ] パフォーマンスへの影響が最小限（キャッシュ利用）

## 設定例
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'post_create': '10/hour',
        'thread_create': '3/hour',
    }
}
```

## 関連タスク
- BE-002: 認証・認可システム（セッション識別に依存）
- BE-004: Redisキャッシュの導入（パフォーマンス向上）
- INF-002: 本番環境でのRedisセットアップ

## 参考
- DRF Throttling: https://www.django-rest-framework.org/api-guide/throttling/
- django-ratelimit: https://django-ratelimit.readthedocs.io/
- django-redis: https://github.com/jazzband/django-redis
