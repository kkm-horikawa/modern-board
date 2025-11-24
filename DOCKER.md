# Docker Setup Guide

このプロジェクトはDockerとDocker Composeを使用して、開発環境と本番環境の両方をサポートしています。

## 前提条件

- Docker Engine 24.0以上
- Docker Compose V2

## クイックスタート

### 開発環境

```bash
# コンテナのビルドと起動
docker compose up -d

# ログの確認
docker compose logs -f

# コンテナの停止
docker compose down
```

アクセス:
- フロントエンド: http://localhost:5173
- バックエンドAPI: http://localhost:8000/api/v1/
- API Documentation (Swagger): http://localhost:8000/api/docs/
- API Documentation (ReDoc): http://localhost:8000/api/redoc/

### 本番環境

```bash
# 環境変数の設定（.envファイルを作成）
cat > .env << EOF
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DEBUG=False
DATABASE_URL=sqlite:////app/db/db.sqlite3
EOF

# 本番環境用のビルドと起動
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# ログの確認
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f
```

## アーキテクチャ

### バックエンド (Django + DRF)

#### マルチステージビルド構成

1. **base**: Python 3.13ベースイメージ、システム依存関係
2. **builder**: uv使用による高速な依存関係インストール
3. **development**: ホットリロード対応の開発サーバー
4. **production**: Gunicorn + 最適化された本番環境

#### 特徴

- Python 3.13使用
- uvによる高速パッケージインストール
- 非rootユーザー(django)で実行
- ヘルスチェック対応
- 永続化ボリューム（DB、static、media）

### フロントエンド (React + Vite)

#### マルチステージビルド構成

1. **base**: Node.js 23、pnpm設定
2. **deps**: 依存関係のインストール（キャッシュ最適化）
3. **builder**: 本番ビルド生成
4. **development**: Vite開発サーバー（HMR対応）
5. **production**: Nginx静的ファイルサーバー

#### 特徴

- Node.js 23 + pnpm使用
- 本番環境はNginx Alpineで軽量化
- セキュリティヘッダー設定済み
- Gzip圧縮、キャッシュ最適化
- SPA routing対応

## コマンドリファレンス

### コンテナ管理

```bash
# ビルド（キャッシュなし）
docker compose build --no-cache

# 特定のサービスのみ起動
docker compose up -d backend
docker compose up -d frontend

# サービスの再起動
docker compose restart backend

# コンテナに入る
docker compose exec backend bash
docker compose exec frontend sh

# ログの確認
docker compose logs -f backend
docker compose logs -f frontend
```

### Django管理コマンド

```bash
# マイグレーション作成
docker compose exec backend python manage.py makemigrations

# マイグレーション実行
docker compose exec backend python manage.py migrate

# スーパーユーザー作成
docker compose exec backend python manage.py createsuperuser

# 静的ファイル収集
docker compose exec backend python manage.py collectstatic --noinput

# Djangoシェル
docker compose exec backend python manage.py shell

# テスト実行
docker compose exec backend pytest
```

### フロントエンド管理コマンド

```bash
# 依存関係の追加
docker compose exec frontend pnpm add <package-name>

# 依存関係の追加（開発用）
docker compose exec frontend pnpm add -D <package-name>

# Lint実行
docker compose exec frontend pnpm run lint

# テスト実行
docker compose exec frontend pnpm run test
```

## ボリューム管理

### ボリューム一覧確認

```bash
docker volume ls | grep modern-board
```

### ボリュームのバックアップ

```bash
# データベースのバックアップ
docker compose exec backend python manage.py dumpdata > backup.json

# メディアファイルのバックアップ
docker run --rm -v modern-board_backend-media:/data -v $(pwd):/backup \
  alpine tar czf /backup/media-backup.tar.gz -C /data .
```

### ボリュームの削除

```bash
# すべてのコンテナとボリュームを削除
docker compose down -v
```

## トラブルシューティング

### ポート競合

```bash
# 既に使用されているポートを確認
sudo lsof -i :8000
sudo lsof -i :5173

# docker-compose.ymlのportsセクションを変更
```

### ビルドエラー

```bash
# キャッシュをクリアして再ビルド
docker compose build --no-cache

# Dockerシステム全体のクリーンアップ
docker system prune -a
```

### パーミッションエラー

```bash
# ホストとコンテナのユーザーIDを確認
id -u
docker compose exec backend id -u

# ボリュームの所有権を修正
docker compose exec backend chown -R django:django /app
```

## ベストプラクティス

### 開発環境

- コードの変更は自動的にコンテナ内に反映されます
- `docker compose logs -f`でリアルタイムログを確認
- 依存関係追加後は`docker compose restart`で反映

### 本番環境

- 必ず`.env`ファイルで環境変数を管理
- `SECRET_KEY`は強力なランダム文字列を使用
- データベースは外部DB（PostgreSQL等）の使用を推奨
- 静的ファイルはCDN配信を検討
- ログ監視とメトリクス収集を設定

## セキュリティ考慮事項

1. **非rootユーザー**: すべてのコンテナは非rootユーザーで実行
2. **最小権限**: 必要最小限のパッケージのみインストール
3. **セキュリティヘッダー**: フロントエンドNginxで各種ヘッダー設定
4. **ヘルスチェック**: コンテナの健全性を自動監視
5. **環境変数**: 機密情報は環境変数で管理

## パフォーマンス最適化

### イメージサイズ削減

- マルチステージビルドで不要なレイヤーを削除
- slim/alpineベースイメージ使用
- .dockerignoreで不要ファイルを除外

### ビルド高速化

- レイヤーキャッシュを活用
- 依存関係のインストールを先に実行
- uvとpnpmで高速インストール

### 実行時最適化

- Gunicornワーカー数の調整（CPU数 × 2 + 1が目安）
- Nginxでgzip圧縮とキャッシュ設定
- ボリュームマウントの最適化
