# DOC-001: 開発環境セットアップガイドの作成

## 概要
新しい開発者がプロジェクトに参加した際に、迅速に開発環境をセットアップできるドキュメントを作成する。

## 優先度
**High** - チーム開発に必須

## 難易度
**Easy** - ドキュメント作成

## 前提条件
- [x] 開発環境が構築されている
- [x] Docker環境が整っている

## 実装内容

### 1. README.mdの作成/更新
- [ ] プロジェクト概要
  - アプリケーションの説明
  - 主要機能
  - 技術スタック
- [ ] 必要な環境
  - OS要件
  - ソフトウェア要件
- [ ] クイックスタート
- [ ] ライセンス情報

### 2. DEVELOPMENT.mdの作成
#### 2.1 必須ソフトウェアのインストール手順
- [ ] Python 3.13のインストール
  ```bash
  # macOS (Homebrew)
  brew install python@3.13

  # Ubuntu
  sudo apt update
  sudo apt install python3.13 python3.13-venv

  # Windows
  # https://www.python.org/downloads/ からダウンロード
  ```
- [ ] uvのインストール
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- [ ] Node.js 20のインストール
  ```bash
  # macOS (Homebrew)
  brew install node@20

  # Ubuntu (NodeSource)
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
  sudo apt install -y nodejs

  # Windows
  # https://nodejs.org/ からダウンロード
  ```
- [ ] Dockerのインストール
  ```bash
  # macOS
  brew install --cask docker

  # Ubuntu
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh

  # Windows
  # https://docs.docker.com/desktop/install/windows-install/
  ```
- [ ] Gitの設定
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```

#### 2.2 プロジェクトのセットアップ
- [ ] リポジトリのクローン
  ```bash
  git clone https://github.com/user/modern-board.git
  cd modern-board
  ```
- [ ] バックエンドのセットアップ
  ```bash
  cd backend
  uv sync --extra dev
  cp .env.example .env  # 環境変数の設定
  uv run python manage.py migrate
  uv run python manage.py createsuperuser
  uv run python manage.py runserver
  ```
- [ ] フロントエンドのセットアップ
  ```bash
  cd frontend
  npm install
  cp .env.example .env  # 環境変数の設定
  npm run dev
  ```
- [ ] Dockerでのセットアップ
  ```bash
  docker-compose up -d
  docker-compose exec backend python manage.py migrate
  docker-compose exec backend python manage.py createsuperuser
  ```

#### 2.3 開発サーバーの起動方法
- [ ] バックエンド（Django）
  ```bash
  cd backend
  uv run python manage.py runserver
  # http://localhost:8000
  ```
- [ ] フロントエンド（Vite）
  ```bash
  cd frontend
  npm run dev
  # http://localhost:5173
  ```
- [ ] Docker Compose
  ```bash
  docker-compose up
  # Backend: http://localhost:8000
  # Frontend: http://localhost:5173
  ```

#### 2.4 テストの実行方法
- [ ] バックエンドテスト
  ```bash
  cd backend
  uv run pytest
  uv run pytest --cov  # カバレッジ付き
  uv run pytest -v api/tests/unit/test_models.py  # 特定のテスト
  ```
- [ ] フロントエンドテスト
  ```bash
  cd frontend
  npm run test
  npm run test:coverage
  npm run test:watch  # ウォッチモード
  ```
- [ ] E2Eテスト
  ```bash
  cd frontend
  npm run test:e2e
  ```

#### 2.5 コード品質チェック
- [ ] バックエンド
  ```bash
  cd backend
  uv run ruff check .  # Lint
  uv run ruff format .  # Format
  uv run pyright  # 型チェック
  uv run pre-commit run --all-files  # Pre-commit hooks
  ```
- [ ] フロントエンド
  ```bash
  cd frontend
  npm run lint
  npm run format
  npm run type-check
  ```

#### 2.6 データベース操作
- [ ] マイグレーションの作成
  ```bash
  uv run python manage.py makemigrations
  ```
- [ ] マイグレーションの適用
  ```bash
  uv run python manage.py migrate
  ```
- [ ] マイグレーションの取り消し
  ```bash
  uv run python manage.py migrate app_name migration_name
  ```
- [ ] データベースのリセット
  ```bash
  rm db.sqlite3
  uv run python manage.py migrate
  uv run python manage.py createsuperuser
  ```

#### 2.7 便利なコマンド
- [ ] Djangoシェル
  ```bash
  uv run python manage.py shell
  ```
- [ ] データのインポート/エクスポート
  ```bash
  uv run python manage.py dumpdata > data.json
  uv run python manage.py loaddata data.json
  ```
- [ ] 静的ファイルの収集
  ```bash
  uv run python manage.py collectstatic
  ```

### 3. CONTRIBUTING.mdの作成
- [ ] コントリビューション方法
- [ ] ブランチ戦略
  ```
  main - 本番環境
  develop - 開発環境
  feature/* - 機能開発
  bugfix/* - バグ修正
  hotfix/* - 緊急修正
  ```
- [ ] コミットメッセージ規約
  ```
  feat: 新機能
  fix: バグ修正
  docs: ドキュメント
  style: フォーマット
  refactor: リファクタリング
  test: テスト
  chore: その他
  ```
- [ ] プルリクエストの作成方法
- [ ] コードレビューのプロセス

### 4. トラブルシューティングガイド
- [ ] よくある問題と解決方法
  - ポートが既に使用されている
  - データベース接続エラー
  - npm installエラー
  - Docker関連のエラー
- [ ] ログの確認方法
- [ ] キャッシュのクリア方法

### 5. 環境変数の説明
- [ ] `.env.example`の作成と説明
  ```env
  # Django
  DJANGO_SECRET_KEY=your-secret-key-here
  DJANGO_DEBUG=True
  DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

  # Database
  DATABASE_URL=postgresql://user:password@localhost:5432/dbname

  # Frontend
  VITE_API_URL=http://localhost:8000/api
  ```
- [ ] 各変数の説明
- [ ] 開発/本番環境での違い

### 6. プロジェクト構造の説明
- [ ] ディレクトリ構成図
  ```
  modern-board/
  ├── backend/
  │   ├── api/           # APIアプリケーション
  │   ├── config/        # Django設定
  │   └── tests/         # テスト
  ├── frontend/
  │   ├── src/
  │   │   ├── components/  # コンポーネント
  │   │   ├── pages/       # ページ
  │   │   └── services/    # API通信
  │   └── e2e/           # E2Eテスト
  └── docs/
      └── tasks/         # タスク管理
  ```
- [ ] 各ディレクトリの役割説明

### 7. デバッグ方法
- [ ] VSCode設定例（`.vscode/launch.json`）
- [ ] pdbの使い方
- [ ] ブラウザDevToolsの活用
- [ ] Django Debug Toolbarの使用

### 8. その他のドキュメント
- [ ] APIドキュメントへのリンク
- [ ] デザインガイドラインへのリンク
- [ ] チームコミュニケーションチャネル

## 受け入れ基準
- [ ] README.mdが作成されている
- [ ] DEVELOPMENT.mdが作成されている
- [ ] CONTRIBUTING.mdが作成されている
- [ ] 新しい開発者がドキュメントを見て環境構築できる
- [ ] トラブルシューティング情報が充実している
- [ ] すべての手順が検証済み
- [ ] スクリーンショットや図が含まれている（必要に応じて）

## ドキュメント配置
```
modern-board/
├── README.md                # プロジェクト概要
├── docs/
│   ├── DEVELOPMENT.md       # 開発環境セットアップ
│   ├── CONTRIBUTING.md      # コントリビューションガイド
│   ├── DEPLOYMENT.md        # デプロイ手順
│   └── tasks/               # タスク管理
└── .env.example             # 環境変数テンプレート
```

## 関連タスク
- すべてのタスク（開発の入り口となるため）

## 参考
- Good README Template: https://github.com/othneildrew/Best-README-Template
- Contributing Guide: https://github.com/nayafia/contributing-template
- Documentation Guide: https://www.writethedocs.org/guide/
