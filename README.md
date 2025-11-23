# Modern Board

モダンな技術スタックで構築した掲示板アプリケーション

## 技術スタック

### バックエンド
- Python 3.11+
- Wagtail 7.2+
- Django 5.2+
- Django REST Framework 3.16+
- pytest 8.0+ (テストフレームワーク)
- Ruff 0.14+ (リンター・フォーマッタ)
- uv (パッケージマネージャー)

### フロントエンド
- TypeScript 5.9+
- React 18.3+
- Vite 7.1+ (ビルドツール)
- Vitest 4.0+ (テストフレームワーク)
- Biome 2.2+ (リンター・フォーマッタ)
- Tailwind CSS 4.0+
- npm (パッケージマネージャー)

## プロジェクト構成

```
.
├── backend/               # Django REST API
│   ├── api/              # メインアプリケーション
│   ├── config/           # Django設定
│   ├── manage.py
│   └── pyproject.toml
├── frontend/              # React + Vite SPA
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── vite.config.ts
├── .vscode/               # VSCode設定
├── .pre-commit-config.yaml
└── README.md
```

## セットアップ

### 必須ツール

1. Python 3.11以上
2. Node.js 20以上
3. uv (Python パッケージマネージャー)
4. Git

### バックエンド環境構築

```bash
cd backend

# 仮想環境作成（自動で.venvディレクトリに作成されます）
uv venv

# 依存関係インストール（開発用を含む）
uv pip install -e ".[dev]"

# マイグレーション実行
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py migrate

# 開発サーバー起動
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py runserver
```

### フロントエンド環境構築

```bash
cd frontend

# 依存関係インストール
npm install

# 開発サーバー起動
npm run dev
```

開発サーバーは `http://localhost:5173` で起動します。

### pre-commit設定

```bash
# ルートディレクトリで実行
pip install pre-commit
pre-commit install

# 手動実行
pre-commit run --all-files
```

## 開発コマンド

### バックエンド

```bash
# テスト実行
pytest

# カバレッジ付きテスト実行
pytest --cov=api --cov-report=html

# Lintチェック
ruff check .

# Lint自動修正
ruff check --fix .

# フォーマット
ruff format .
```

### フロントエンド

```bash
# 開発サーバー起動
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
```

## コーディング規約

詳細なコーディング規約については、プロジェクトルートの `CODING_STANDARDS.md` を参照してください。

### 主要なルール

**Python**:
- 行の長さ: 最大88文字
- インデント: スペース4つ
- 文字列: ダブルクォート `"`
- 型アノテーション必須

**TypeScript/React**:
- 行の長さ: 最大100文字
- インデント: スペース2つ
- 文字列: ダブルクォート `"`
- セミコロン必須

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
