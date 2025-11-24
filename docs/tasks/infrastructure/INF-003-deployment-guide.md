# INF-003: 本番環境デプロイ手順書の作成

## 概要
本番環境へのデプロイ手順を文書化し、再現可能で安全なデプロイプロセスを確立する。

## 優先度
**Medium** - 初回デプロイ前に必要

## 難易度
**Easy** - ドキュメント作成

## 前提条件
- [x] INF-001: 本番用Docker Compose設定が完了
- [x] INF-002: CI/CDパイプラインが構築済み
- [ ] デプロイ先サーバーが決定している

## 実装内容

### 1. デプロイ先の選定と設定
- [ ] デプロイ先の決定（AWS, GCP, Azure, VPS等）
- [ ] サーバースペックの決定
  - CPU: 2コア以上推奨
  - メモリ: 4GB以上推奨
  - ストレージ: 20GB以上推奨
- [ ] OSのインストール（Ubuntu 22.04 LTS推奨）
- [ ] ドメインの取得と設定

### 2. サーバー初期セットアップ手順
- [ ] SSHキー認証の設定
  ```bash
  # ローカル
  ssh-keygen -t ed25519 -C "your_email@example.com"
  ssh-copy-id user@server_ip

  # サーバー
  sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
  sudo systemctl restart sshd
  ```
- [ ] ファイアウォール設定（UFW）
  ```bash
  sudo ufw allow 22/tcp
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw enable
  ```
- [ ] タイムゾーン設定
  ```bash
  sudo timedatectl set-timezone Asia/Tokyo
  ```
- [ ] ユーザー作成（sudo権限付与）
  ```bash
  sudo adduser deploy
  sudo usermod -aG sudo deploy
  ```

### 3. 必要なソフトウェアのインストール
- [ ] Docker のインストール
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker $USER
  ```
- [ ] Docker Compose のインストール
  ```bash
  sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  ```
- [ ] Git のインストール
  ```bash
  sudo apt update
  sudo apt install git -y
  ```
- [ ] その他必要なツール
  ```bash
  sudo apt install curl wget vim htop -y
  ```

### 4. アプリケーションのデプロイ
- [ ] リポジトリのクローン
  ```bash
  cd /opt
  sudo git clone https://github.com/user/modern-board.git
  sudo chown -R deploy:deploy modern-board
  cd modern-board
  ```
- [ ] 環境変数の設定
  ```bash
  cp .env.production.example .env.production
  vim .env.production  # 必要な値を設定
  ```
- [ ] Docker Composeでビルド
  ```bash
  docker-compose -f docker-compose.production.yml build
  ```
- [ ] データベースマイグレーション
  ```bash
  docker-compose -f docker-compose.production.yml run --rm backend python manage.py migrate
  ```
- [ ] 静的ファイルの収集
  ```bash
  docker-compose -f docker-compose.production.yml run --rm backend python manage.py collectstatic --noinput
  ```
- [ ] スーパーユーザーの作成
  ```bash
  docker-compose -f docker-compose.production.yml run --rm backend python manage.py createsuperuser
  ```
- [ ] コンテナの起動
  ```bash
  docker-compose -f docker-compose.production.yml up -d
  ```

### 5. SSL/TLS証明書の設定（Let's Encrypt）
- [ ] Certbotのインストール
  ```bash
  sudo apt install certbot python3-certbot-nginx -y
  ```
- [ ] 証明書の取得
  ```bash
  sudo certbot --nginx -d example.com -d www.example.com
  ```
- [ ] 自動更新の設定
  ```bash
  sudo certbot renew --dry-run
  ```
- [ ] Nginxの再起動
  ```bash
  docker-compose -f docker-compose.production.yml restart nginx
  ```

### 6. モニタリングとアラート設定
- [ ] ログの確認方法
  ```bash
  docker-compose -f docker-compose.production.yml logs -f backend
  docker-compose -f docker-compose.production.yml logs -f nginx
  ```
- [ ] ヘルスチェックの設定
- [ ] アラート設定（ディスク使用率、CPU使用率等）
- [ ] Uptime監視（UptimeRobot等）

### 7. バックアップ戦略
- [ ] データベースバックアップスクリプト
  ```bash
  #!/bin/bash
  BACKUP_DIR="/backups/postgres"
  DATE=$(date +%Y%m%d_%H%M%S)
  docker-compose -f docker-compose.production.yml exec -T db pg_dump -U postgres modern_board > $BACKUP_DIR/backup_$DATE.sql
  # 古いバックアップの削除（7日以上前）
  find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
  ```
- [ ] Cronでの自動実行
  ```bash
  0 2 * * * /opt/modern-board/scripts/backup_db.sh
  ```
- [ ] メディアファイルのバックアップ
- [ ] バックアップの保存先（S3等）

### 8. デプロイスクリプトの作成
- [ ] `deploy.sh`の作成
  ```bash
  #!/bin/bash
  set -e

  echo "Pulling latest changes..."
  git pull origin main

  echo "Building containers..."
  docker-compose -f docker-compose.production.yml build

  echo "Running migrations..."
  docker-compose -f docker-compose.production.yml run --rm backend python manage.py migrate

  echo "Collecting static files..."
  docker-compose -f docker-compose.production.yml run --rm backend python manage.py collectstatic --noinput

  echo "Restarting containers..."
  docker-compose -f docker-compose.production.yml up -d

  echo "Deployment complete!"
  ```
- [ ] ロールバックスクリプトの作成

### 9. セキュリティ設定
- [ ] Fail2Banのインストールと設定
  ```bash
  sudo apt install fail2ban -y
  sudo systemctl enable fail2ban
  ```
- [ ] ログ監視の設定
- [ ] 定期的なセキュリティアップデート
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
- [ ] Docker Benchmarkの実行

### 10. パフォーマンスチューニング
- [ ] PostgreSQLのチューニング
- [ ] Nginxのチューニング
- [ ] Gunicornワーカー数の調整
- [ ] Redisのメモリ設定

### 11. ドキュメント作成
- [ ] `docs/DEPLOYMENT.md` の作成
  - サーバー要件
  - 初期セットアップ手順
  - デプロイ手順
  - トラブルシューティング
  - ロールバック手順
  - バックアップ/リストア手順
- [ ] 環境変数一覧の文書化
- [ ] デプロイチェックリストの作成

## 受け入れ基準
- [ ] 本番環境にデプロイできる
- [ ] SSL/TLS証明書が設定されている
- [ ] データベースバックアップが自動実行される
- [ ] ログが適切に記録される
- [ ] モニタリングが機能している
- [ ] デプロイ手順が文書化されている
- [ ] ロールバックが可能
- [ ] セキュリティ設定が完了している

## デプロイチェックリスト
```markdown
## デプロイ前
- [ ] すべてのテストがパスしている
- [ ] 環境変数が設定されている
- [ ] データベースバックアップが取得されている
- [ ] デプロイ計画が共有されている

## デプロイ中
- [ ] メンテナンスモードを有効化
- [ ] 最新コードをpull
- [ ] Dockerイメージのビルド
- [ ] データベースマイグレーション
- [ ] 静的ファイルの収集
- [ ] コンテナの再起動

## デプロイ後
- [ ] アプリケーションが起動している
- [ ] ヘルスチェックがパスする
- [ ] 主要機能の動作確認
- [ ] ログにエラーがないか確認
- [ ] メンテナンスモードを無効化
- [ ] モニタリングダッシュボードの確認
```

## トラブルシューティング
### コンテナが起動しない
```bash
# ログ確認
docker-compose -f docker-compose.production.yml logs

# コンテナの状態確認
docker-compose -f docker-compose.production.yml ps

# コンテナの再ビルド
docker-compose -f docker-compose.production.yml build --no-cache
```

### データベース接続エラー
```bash
# PostgreSQLコンテナの確認
docker-compose -f docker-compose.production.yml exec db psql -U postgres -c "SELECT version();"

# 環境変数の確認
docker-compose -f docker-compose.production.yml exec backend env | grep DATABASE
```

## 関連タスク
- INF-001: 本番用Docker Compose設定
- INF-002: CI/CDパイプライン
- BE-006: エラーハンドリング・ロギング

## 参考
- Docker Deployment: https://docs.docker.com/compose/production/
- Let's Encrypt: https://letsencrypt.org/getting-started/
- PostgreSQL Backup: https://www.postgresql.org/docs/current/backup.html
- Security Best Practices: https://cheatsheetseries.owasp.org/
