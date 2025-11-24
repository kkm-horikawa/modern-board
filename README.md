# Modern Board

モダンな技術スタックで構築した匿名掲示板アプリケーション

## 概要

Modern Boardは、現代的な技術スタックを使用して構築された匿名掲示板アプリケーションです。バックエンドにDjango REST Framework、フロントエンドにReact + TypeScriptを採用し、高速で保守性の高いWebアプリケーションを実現しています。

### 主要機能

- スレッド作成・閲覧
- 返信機能
- リアルタイム更新
- レスポンシブデザイン
- RESTful API

## 技術スタック

### バックエンド
- **Python** 3.13+
- **Django** 5.2+
- **Wagtail** 7.2+
- **Django REST Framework** 3.16+
- **pytest** 8.0+ (テストフレームワーク)
- **Ruff** 0.14+ (リンター・フォーマッタ)
- **uv** (パッケージマネージャー)

### フロントエンド
- **TypeScript** 5.9+
- **React** 19.2+
- **Vite** 7.2+ (ビルドツール)
- **Vitest** 4.0+ (テストフレームワーク)
- **Biome** 2.3+ (リンター・フォーマッタ)
- **Tailwind CSS** 4.0+
- **npm** (パッケージマネージャー)

### インフラ
- **Docker** & **Docker Compose**
- **SQLite** (開発環境)
- **Gunicorn** (本番環境)
- **Nginx** (本番環境)

## クイックスタート

### 必須環境

- Python 3.13以上
- Node.js 20以上
- uv (Python パッケージマネージャー)
- Git

### セットアップ

#### 1. リポジトリのクローン

```bash
git clone https://github.com/kkm-horikawa/modern-board.git
cd modern-board
```

#### 2. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成と依存関係のインストール
uv sync --extra dev

# マイグレーションの実行
uv run python manage.py migrate

# 開発サーバーの起動
uv run python manage.py runserver
```

バックエンドは `http://localhost:8000` で起動します。

#### 3. フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev
```

フロントエンドは `http://localhost:5173` で起動します。

## Dockerでの起動

```bash
# コンテナのビルドと起動
docker compose up -d

# ログの確認
docker compose logs -f

# 初回のみ: マイグレーションとスーパーユーザー作成
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

詳細は [DOCKER.md](./DOCKER.md) を参照してください。

## プロジェクト構成

```
modern-board/
├── backend/               # Django REST API
│   ├── api/              # メインアプリケーション
│   │   ├── models/       # データモデル
│   │   ├── serializers/  # シリアライザー
│   │   ├── views/        # ビュー
│   │   └── tests/        # テスト
│   ├── config/           # Django設定
│   │   ├── settings/     # 環境別設定
│   │   │   ├── base.py   # 基本設定
│   │   │   ├── dev.py    # 開発環境
│   │   │   └── production.py # 本番環境
│   │   └── urls.py       # URLルーティング
│   ├── manage.py         # Django管理コマンド
│   └── pyproject.toml    # Python依存関係
├── frontend/              # React + Vite SPA
│   ├── src/
│   │   ├── components/   # Reactコンポーネント
│   │   ├── pages/        # ページコンポーネント
│   │   ├── services/     # API通信
│   │   └── types/        # TypeScript型定義
│   ├── tests/            # テスト
│   ├── package.json      # npm依存関係
│   └── vite.config.ts    # Vite設定
├── docs/                  # ドキュメント
│   ├── DEVELOPMENT.md    # 開発環境セットアップ
│   ├── CONTRIBUTING.md   # コントリビューションガイド
│   └── tasks/            # タスク管理
├── .vscode/               # VSCode設定
├── .pre-commit-config.yaml
├── docker-compose.yml     # Docker Compose設定
└── README.md
```

## 開発コマンド

### バックエンド

```bash
# テスト実行
cd backend
uv run pytest

# カバレッジ付きテスト実行
uv run pytest --cov=api --cov-report=html

# Lintチェック
uv run ruff check .

# Lint自動修正
uv run ruff check --fix .

# フォーマット
uv run ruff format .

# 型チェック
uv run pyright
```

### フロントエンド

```bash
# 開発サーバー起動
cd frontend
npm run dev

# ビルド
npm run build

# Lintチェック
npm run lint

# Lint自動修正
npm run lint:fix

# フォーマット
npm run format

# テスト実行
npm test

# カバレッジ付きテスト実行
npm run test:coverage

# テスト（ウォッチモード）
npm run test:watch
```

## 詳細なドキュメント

- [開発環境セットアップガイド](./docs/DEVELOPMENT.md) - 詳細なセットアップ手順とトラブルシューティング
- [コントリビューションガイド](./docs/CONTRIBUTING.md) - 開発への参加方法
- [Docker セットアップガイド](./DOCKER.md) - Dockerを使用した環境構築
- [タスク管理](./docs/tasks/README.md) - プロジェクトのタスクと進捗

## API ドキュメント

バックエンドを起動後、以下のURLでAPIドキュメントにアクセスできます：

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## コーディング規約

### Python
- 行の長さ: 最大88文字
- インデント: スペース4つ
- 文字列: ダブルクォート `"`
- 型アノテーション必須

### TypeScript/React
- 行の長さ: 最大100文字
- インデント: スペース2つ
- 文字列: ダブルクォート `"`
- セミコロン必須

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](./LICENSE) を参照してください。

## コントリビューション

プロジェクトへの貢献を歓迎します！詳細は [CONTRIBUTING.md](./docs/CONTRIBUTING.md) を参照してください。

## サポート

問題が発生した場合は、[GitHub Issues](https://github.com/kkm-horikawa/modern-board/issues) で報告してください。
