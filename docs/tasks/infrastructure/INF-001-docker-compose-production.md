# INF-001: 本番用Docker Compose設定

## 概要
本番環境向けのDocker Compose設定を作成し、マルチステージビルド、環境変数管理、セキュリティ対策を実装する。

## 優先度
**Medium** - デプロイ前に必要

## 難易度
**Medium**

## 前提条件
- [x] 開発用Docker環境が構築済み
- [x] バックエンドとフロントエンドの実装が完了
- [ ] 本番環境のインフラ構成が決定している

## 実装内容

### 1. マルチステージDockerfile（バックエンド）
- [ ] ベースイメージの最適化（python:3.13-slim-alpine等）
- [ ] ビルドステージと実行ステージの分離
- [ ] 不要なファイルの除外（.dockerignore）
- [ ] セキュリティスキャン対応
- [ ] ヘルスチェックの実装

**Dockerfile.production例:**
```dockerfile
# Build stage
FROM python:3.13-slim as builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

# Runtime stage
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application"]
```

### 2. マルチステージDockerfile（フロントエンド）
- [ ] Node.js ベースイメージ
- [ ] ビルドステージでのViteビルド
- [ ] Nginxステージでの静的ファイル配信
- [ ] Nginx設定の最適化
- [ ] Gzip圧縮の有効化

**Dockerfile.production例:**
```dockerfile
# Build stage
FROM node:20-alpine as builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### 3. 本番用docker-compose.yml
- [ ] PostgreSQL サービス（本番用）
- [ ] Redis サービス
- [ ] バックエンド（Gunicorn）
- [ ] フロントエンド（Nginx）
- [ ] リバースプロキシ（Nginx）
- [ ] ボリューム設定（データ永続化）
- [ ] ネットワーク設定
- [ ] ヘルスチェック設定

### 4. 環境変数管理
- [ ] `.env.production.example`の作成
- [ ] 本番環境の環境変数定義
- [ ] シークレット管理の方針決定
- [ ] Docker Secrets の使用検討

**必要な環境変数:**
```bash
# Django
DJANGO_SECRET_KEY=
DJANGO_ALLOWED_HOSTS=
DJANGO_DEBUG=False
DATABASE_URL=
REDIS_URL=

# PostgreSQL
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

# Frontend
VITE_API_URL=
```

### 5. Gunicorn設定
- [ ] `gunicorn.conf.py`の作成
- [ ] ワーカー数の設定
- [ ] タイムアウト設定
- [ ] ログ設定
- [ ] プロセス管理

### 6. Nginx設定
- [ ] リバースプロキシ設定
- [ ] 静的ファイル配信設定
- [ ] Gzip圧縮
- [ ] キャッシュ設定
- [ ] セキュリティヘッダー
- [ ] SSL/TLS設定（Let's Encrypt対応）
- [ ] レート制限

### 7. データベース設定
- [ ] PostgreSQL の本番用設定
- [ ] 接続プール設定
- [ ] バックアップ戦略
- [ ] マイグレーション戦略

### 8. ロギング設定
- [ ] アプリケーションログの集約
- [ ] ログローテーション
- [ ] ログレベルの設定
- [ ] エラートラッキング（Sentry等）検討

### 9. モニタリング
- [ ] ヘルスチェックエンドポイント
- [ ] メトリクス収集（Prometheus等）検討
- [ ] アラート設定

### 10. セキュリティ対策
- [ ] 最小権限の原則（non-rootユーザー）
- [ ] イメージの脆弱性スキャン
- [ ] セキュリティヘッダーの設定
- [ ] ファイアウォール設定

## 受け入れ基準
- [ ] 本番用Dockerfileが最適化されている
- [ ] docker-compose.ymlが正しく動作する
- [ ] 環境変数が適切に管理されている
- [ ] ヘルスチェックが機能している
- [ ] ログが適切に出力されている
- [ ] セキュリティベストプラクティスに従っている
- [ ] パフォーマンスが良好
- [ ] イメージサイズが最適化されている

## docker-compose.production.yml 例
```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.production
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      DJANGO_SETTINGS_MODULE: config.settings.production
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.production
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/static
      - media_volume:/media
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
```

## 関連タスク
- INF-002: CI/CDパイプラインの構築
- INF-003: 本番環境へのデプロイ
- BE-004: Redisキャッシュの導入

## 参考
- Docker Multi-stage: https://docs.docker.com/build/building/multi-stage/
- Gunicorn: https://docs.gunicorn.org/
- Nginx Best Practices: https://www.nginx.com/blog/nginx-caching-guide/
