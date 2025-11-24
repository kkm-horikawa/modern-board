# INF-002: CI/CDパイプラインの構築

## 概要
GitHub Actionsを使用したCI/CDパイプラインを構築し、テスト、ビルド、デプロイを自動化する。

## 優先度
**Medium** - 開発効率とコード品質に影響

## 難易度
**Medium**

## 前提条件
- [x] GitHubリポジトリが存在する
- [ ] テストが実装されている
- [ ] デプロイ先が決定している

## 実装内容

### 1. CI パイプライン - バックエンド
- [ ] `.github/workflows/backend-ci.yml`の作成
- [ ] Python環境のセットアップ（uv使用）
- [ ] 依存関係のインストール
- [ ] Ruffによるリント
- [ ] Pyrightによる型チェック
- [ ] Pytestによるテスト実行
- [ ] カバレッジレポートの生成
- [ ] テスト結果のアップロード

**backend-ci.yml例:**
```yaml
name: Backend CI

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'backend/**'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v1

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          cd backend
          uv sync --extra dev

      - name: Run ruff
        run: |
          cd backend
          uv run ruff check .

      - name: Run pyright
        run: |
          cd backend
          uv run pyright

      - name: Run tests
        run: |
          cd backend
          uv run pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./backend/coverage.xml
```

### 2. CI パイプライン - フロントエンド
- [ ] `.github/workflows/frontend-ci.yml`の作成
- [ ] Node.js環境のセットアップ
- [ ] 依存関係のインストール（キャッシュ活用）
- [ ] ESLintによるリント
- [ ] TypeScriptの型チェック
- [ ] Vitestによるテスト実行
- [ ] ビルドの確認
- [ ] カバレッジレポートの生成

**frontend-ci.yml例:**
```yaml
name: Frontend CI

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run ESLint
        run: |
          cd frontend
          npm run lint

      - name: Type check
        run: |
          cd frontend
          npm run type-check

      - name: Run tests
        run: |
          cd frontend
          npm run test -- --coverage

      - name: Build
        run: |
          cd frontend
          npm run build

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./frontend/coverage/coverage-final.json
```

### 3. CD パイプライン - デプロイ
- [ ] `.github/workflows/deploy.yml`の作成
- [ ] デプロイ戦略の決定（Blue-Green, Rolling, Canary）
- [ ] Dockerイメージのビルドとプッシュ
- [ ] コンテナレジストリの設定（Docker Hub, GitHub Container Registry, AWS ECR等）
- [ ] デプロイスクリプトの作成
- [ ] 環境変数の管理（GitHub Secrets）

**deploy.yml例:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/Dockerfile.production
          push: true
          tags: ghcr.io/${{ github.repository }}/backend:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build and push frontend
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          file: ./frontend/Dockerfile.production
          push: true
          tags: ghcr.io/${{ github.repository }}/frontend:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_KEY }}
          script: |
            cd /app/modern-board
            docker-compose pull
            docker-compose up -d
            docker-compose exec backend python manage.py migrate
```

### 4. プルリクエストワークフロー
- [ ] PRコメントへのテスト結果投稿
- [ ] カバレッジ変化の表示
- [ ] ビルドサイズの変化通知
- [ ] 自動マージ設定（オプション）

### 5. セキュリティスキャン
- [ ] 依存関係の脆弱性スキャン（Dependabot）
- [ ] Dockerイメージのスキャン（Trivy等）
- [ ] シークレットスキャン（GitGuardian等）
- [ ] コード品質スキャン（SonarQube等、オプション）

### 6. 環境別デプロイ
- [ ] 開発環境（develop branch）
- [ ] ステージング環境（staging branch）
- [ ] 本番環境（main branch）
- [ ] 環境変数の分離

### 7. ロールバック機能
- [ ] 以前のバージョンへの切り戻し手順
- [ ] タグベースデプロイ
- [ ] イメージバージョン管理

### 8. 通知設定
- [ ] デプロイ成功/失敗の通知（Slack, Discord等）
- [ ] テスト失敗の通知
- [ ] セキュリティアラート

## 受け入れ基準
- [ ] すべてのプッシュでCIが実行される
- [ ] テストが失敗した場合、マージがブロックされる
- [ ] mainブランチへのマージで自動デプロイされる
- [ ] カバレッジレポートが生成される
- [ ] セキュリティスキャンが実行される
- [ ] デプロイが成功し、アプリケーションが正常動作する
- [ ] ロールバックが可能
- [ ] CI/CDの実行時間が妥当（15分以内目標）

## GitHub Secrets設定
```
DEPLOY_HOST: デプロイ先サーバーのホスト名
DEPLOY_USER: デプロイ用ユーザー名
DEPLOY_KEY: SSH秘密鍵
DJANGO_SECRET_KEY: Django SECRET_KEY
DATABASE_URL: データベース接続URL
REDIS_URL: Redis接続URL
```

## 関連タスク
- INF-001: 本番用Docker Compose設定
- INF-003: 本番環境へのデプロイ
- BE-001: API統合テスト
- FE-007: フロントエンドテスト

## 参考
- GitHub Actions: https://docs.github.com/en/actions
- Docker Build Push Action: https://github.com/docker/build-push-action
- Codecov: https://about.codecov.io/
- Dependabot: https://docs.github.com/en/code-security/dependabot
