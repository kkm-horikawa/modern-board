# BE-006: エラーハンドリングとロギングの強化

## 概要
統一的なエラーハンドリングとロギングを実装し、本番環境での問題追跡とデバッグを容易にする。

## 優先度
**Medium** - 本番運用前に必要

## 難易度
**Medium**

## 前提条件
- [x] Django とDRFが設定済み
- [x] 基本的なAPIエンドポイントが実装済み

## 実装内容

### 1. カスタム例外ハンドラー
- [ ] DRF用カスタム例外ハンドラーの作成
  ```python
  # api/exceptions.py
  from rest_framework.views import exception_handler
  from rest_framework.response import Response
  import logging

  logger = logging.getLogger(__name__)

  def custom_exception_handler(exc, context):
      response = exception_handler(exc, context)

      if response is not None:
          # ログ記録
          logger.error(
              f"API Error: {exc.__class__.__name__}",
              extra={
                  'status_code': response.status_code,
                  'detail': response.data,
                  'path': context['request'].path,
                  'method': context['request'].method,
              }
          )

          # エラーレスポンスの統一
          response.data = {
              'error': {
                  'code': response.status_code,
                  'message': str(exc),
                  'details': response.data
              }
          }

      return response
  ```
- [ ] `settings.py`に設定を追加
  ```python
  REST_FRAMEWORK = {
      'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',
  }
  ```

### 2. カスタム例外クラスの定義
- [ ] ビジネスロジック用の例外クラス
  ```python
  class ThreadLockedException(APIException):
      status_code = 403
      default_detail = 'このスレッドはロックされています。'
      default_code = 'thread_locked'

  class RateLimitExceeded(APIException):
      status_code = 429
      default_detail = '投稿制限に達しました。しばらくお待ちください。'
      default_code = 'rate_limit_exceeded'

  class InvalidSessionException(APIException):
      status_code = 401
      default_detail = 'セッションが無効です。'
      default_code = 'invalid_session'
  ```
- [ ] 例外クラスの使用例をドキュメント化

### 3. ロギング設定
- [ ] `settings.py`でのロギング設定
  ```python
  LOGGING = {
      'version': 1,
      'disable_existing_loggers': False,
      'formatters': {
          'verbose': {
              'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
              'style': '{',
          },
          'simple': {
              'format': '{levelname} {message}',
              'style': '{',
          },
          'json': {
              '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
              'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
          },
      },
      'filters': {
          'require_debug_false': {
              '()': 'django.utils.log.RequireDebugFalse',
          },
      },
      'handlers': {
          'console': {
              'class': 'logging.StreamHandler',
              'formatter': 'verbose',
          },
          'file': {
              'class': 'logging.handlers.RotatingFileHandler',
              'filename': 'logs/django.log',
              'maxBytes': 1024 * 1024 * 10,  # 10MB
              'backupCount': 5,
              'formatter': 'verbose',
          },
          'error_file': {
              'level': 'ERROR',
              'class': 'logging.handlers.RotatingFileHandler',
              'filename': 'logs/errors.log',
              'maxBytes': 1024 * 1024 * 10,
              'backupCount': 5,
              'formatter': 'verbose',
          },
      },
      'loggers': {
          'django': {
              'handlers': ['console', 'file'],
              'level': 'INFO',
          },
          'django.request': {
              'handlers': ['error_file'],
              'level': 'ERROR',
              'propagate': False,
          },
          'api': {
              'handlers': ['console', 'file', 'error_file'],
              'level': 'DEBUG',
              'propagate': False,
          },
      },
  }
  ```
- [ ] JSON形式ログの設定（本番環境用）
- [ ] ログローテーションの設定

### 4. ロギングの実装
- [ ] ViewSetでのロギング
  ```python
  import logging

  logger = logging.getLogger(__name__)

  class ThreadViewSet(viewsets.ModelViewSet):
      def create(self, request, *args, **kwargs):
          logger.info(
              f"Thread creation attempt",
              extra={
                  'user_session': request.session.session_key,
                  'ip': request.META.get('REMOTE_ADDR'),
              }
          )
          try:
              response = super().create(request, *args, **kwargs)
              logger.info(f"Thread created: {response.data['id']}")
              return response
          except Exception as e:
              logger.error(f"Thread creation failed: {str(e)}")
              raise
  ```
- [ ] 重要な操作のロギング
  - スレッド作成
  - 投稿作成
  - リアクション追加
  - 管理操作（ロック、ピン留め等）

### 5. エラートラッキング（Sentry統合、オプション）
- [ ] Sentryのインストール
  ```bash
  uv add sentry-sdk
  ```
- [ ] Sentryの設定
  ```python
  import sentry_sdk
  from sentry_sdk.integrations.django import DjangoIntegration

  sentry_sdk.init(
      dsn=os.environ.get('SENTRY_DSN'),
      integrations=[DjangoIntegration()],
      traces_sample_rate=0.1,
      send_default_pii=False,
      environment=os.environ.get('ENVIRONMENT', 'development'),
  )
  ```
- [ ] 環境変数での管理

### 6. バリデーションエラーの統一
- [ ] DRF Serializerエラーのフォーマット統一
- [ ] 分かりやすいエラーメッセージ
- [ ] 国際化対応（日本語エラーメッセージ）

### 7. ヘルスチェックエンドポイント
- [ ] `/health/` エンドポイントの実装
  ```python
  from rest_framework.decorators import api_view
  from rest_framework.response import Response
  from django.db import connection

  @api_view(['GET'])
  def health_check(request):
      try:
          # データベース接続チェック
          connection.ensure_connection()

          return Response({
              'status': 'healthy',
              'database': 'connected',
          })
      except Exception as e:
          logger.error(f"Health check failed: {str(e)}")
          return Response({
              'status': 'unhealthy',
              'error': str(e)
          }, status=503)
  ```
- [ ] データベース接続チェック
- [ ] Redis接続チェック（導入後）

### 8. パフォーマンスモニタリング
- [ ] スロークエリのログ記録
- [ ] リクエスト/レスポンス時間の計測
- [ ] ミドルウェアでのモニタリング（オプション）

### 9. セキュリティロギング
- [ ] 認証失敗のログ記録
- [ ] レート制限超過のログ記録
- [ ] 疑わしいアクティビティの検出

### 10. テスト
- [ ] 例外ハンドラーのテスト
- [ ] カスタム例外のテスト
- [ ] ロギングのテスト（ログ出力の確認）

## 受け入れ基準
- [ ] カスタム例外ハンドラーが動作している
- [ ] エラーレスポンスが統一されている
- [ ] ログが適切なレベルで記録されている
- [ ] ログローテーションが機能している
- [ ] ヘルスチェックエンドポイントが動作する
- [ ] 本番環境でのログ確認が容易
- [ ] Sentry統合が動作する（導入する場合）

## ログレベルの使い分け
- **DEBUG**: 開発時の詳細情報
- **INFO**: 通常の操作（スレッド作成、投稿作成等）
- **WARNING**: 警告レベルの問題（レート制限等）
- **ERROR**: エラー（例外発生等）
- **CRITICAL**: 致命的なエラー（システムダウン等）

## エラーレスポンスフォーマット
```json
{
  "error": {
    "code": 400,
    "message": "バリデーションエラー",
    "details": {
      "title": ["この項目は必須です。"],
      "category": ["有効なカテゴリを選択してください。"]
    }
  }
}
```

## 関連タスク
- BE-002: 認証・認可システム（セキュリティロギング）
- BE-003: スパム対策・レート制限（レート制限ロギング）
- INF-001: 本番用Docker設定（ログの永続化）

## 参考
- Django Logging: https://docs.djangoproject.com/en/5.2/topics/logging/
- DRF Exception Handling: https://www.django-rest-framework.org/api-guide/exceptions/
- Sentry: https://docs.sentry.io/platforms/python/guides/django/
- Python Logging: https://docs.python.org/3/library/logging.html
