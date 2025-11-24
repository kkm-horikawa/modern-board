# 開発環境セットアップガイド

このドキュメントは、Modern Boardプロジェクトの開発環境をセットアップするための詳細なガイドです。

## 目次

- [必須ソフトウェアのインストール](#必須ソフトウェアのインストール)
- [プロジェクトのセットアップ](#プロジェクトのセットアップ)
- [開発サーバーの起動](#開発サーバーの起動)
- [テストの実行](#テストの実行)
- [コード品質チェック](#コード品質チェック)
- [データベース操作](#データベース操作)
- [便利なコマンド](#便利なコマンド)
- [環境変数](#環境変数)
- [デバッグ方法](#デバッグ方法)
- [トラブルシューティング](#トラブルシューティング)

## 必須ソフトウェアのインストール

### Python 3.13

#### macOS (Homebrew)
```bash
brew install python@3.13
```

#### Ubuntu
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

#### Windows
[Python公式サイト](https://www.python.org/downloads/)からインストーラーをダウンロードしてインストールしてください。

インストール確認:
```bash
python3 --version
# Python 3.13.x が表示されることを確認
```

### uv（Python パッケージマネージャー）

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

インストール確認:
```bash
uv --version
```

### Node.js 20

#### macOS (Homebrew)
```bash
brew install node@20
```

#### Ubuntu (NodeSource)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

#### Windows
[Node.js公式サイト](https://nodejs.org/)からLTS版をダウンロードしてインストールしてください。

インストール確認:
```bash
node --version
# v20.x.x が表示されることを確認

npm --version
# 10.x.x が表示されることを確認
```

### Docker（オプション）

Docker環境での開発を希望する場合にインストールしてください。

#### macOS
```bash
brew install --cask docker
```

#### Ubuntu
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# ログアウト/ログインして権限を反映
```

#### Windows
[Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)をインストールしてください。

インストール確認:
```bash
docker --version
docker compose version
```

### Git

ほとんどの環境ではデフォルトでインストールされていますが、未インストールの場合：

#### macOS
```bash
brew install git
```

#### Ubuntu
```bash
sudo apt install git
```

#### Windows
[Git for Windows](https://git-scm.com/download/win)をインストールしてください。

Git設定:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## プロジェクトのセットアップ

### リポジトリのクローン

```bash
git clone https://github.com/kkm-horikawa/modern-board.git
cd modern-board
```

### バックエンドのセットアップ

```bash
cd backend

# 依存関係のインストール（開発用を含む）
uv sync --extra dev

# 環境変数の設定（後述の環境変数セクション参照）
# .env.example をコピーして .env を作成
cp .env.example .env

# マイグレーションの実行
uv run python manage.py migrate

# スーパーユーザーの作成（管理画面用）
uv run python manage.py createsuperuser

# 開発サーバーの起動
uv run python manage.py runserver
```

バックエンドが正常に起動すると、以下のURLでアクセスできます：
- API: http://localhost:8000/api/v1/
- 管理画面: http://localhost:8000/admin/
- API ドキュメント (Swagger): http://localhost:8000/api/docs/
- API ドキュメント (ReDoc): http://localhost:8000/api/redoc/

### フロントエンドのセットアップ

新しいターミナルウィンドウを開いて：

```bash
cd frontend

# 依存関係のインストール
npm install

# 環境変数の設定（後述の環境変数セクション参照）
# .env.example をコピーして .env を作成
cp .env.example .env

# 開発サーバーの起動
npm run dev
```

フロントエンドが正常に起動すると、http://localhost:5173 でアクセスできます。

### Dockerでのセットアップ（オプション）

Docker環境で開発する場合：

```bash
# コンテナのビルドと起動
docker compose up -d

# ログの確認
docker compose logs -f

# マイグレーションの実行
docker compose exec backend python manage.py migrate

# スーパーユーザーの作成
docker compose exec backend python manage.py createsuperuser
```

詳細は [DOCKER.md](../DOCKER.md) を参照してください。

### pre-commit フックの設定（推奨）

コミット前に自動的にコード品質チェックを実行するように設定します：

```bash
# ルートディレクトリで実行
uv tool install pre-commit
pre-commit install

# 手動実行（全ファイル対象）
pre-commit run --all-files
```

## 開発サーバーの起動

### バックエンド（Django）

```bash
cd backend
uv run python manage.py runserver

# または特定のポートで起動
uv run python manage.py runserver 8080
```

起動後のアクセス先:
- API: http://localhost:8000/api/v1/
- 管理画面: http://localhost:8000/admin/
- Swagger UI: http://localhost:8000/api/docs/

### フロントエンド（Vite）

```bash
cd frontend
npm run dev

# または特定のポートで起動
npm run dev -- --port 3000
```

起動後のアクセス先:
- フロントエンド: http://localhost:5173

### Docker Compose

```bash
docker compose up

# バックグラウンドで起動
docker compose up -d

# 特定のサービスのみ起動
docker compose up backend
docker compose up frontend
```

起動後のアクセス先:
- バックエンドAPI: http://localhost:8000/api/v1/
- フロントエンド: http://localhost:5173

## テストの実行

### バックエンドテスト

```bash
cd backend

# すべてのテストを実行
uv run pytest

# カバレッジ付きで実行
uv run pytest --cov=api --cov-report=html

# 特定のテストファイルを実行
uv run pytest api/tests/unit/test_models.py

# 特定のテストクラスを実行
uv run pytest api/tests/unit/test_models.py::TestBoardModel

# 特定のテスト関数を実行
uv run pytest api/tests/unit/test_models.py::TestBoardModel::test_board_creation

# 詳細な出力で実行
uv run pytest -v

# 失敗したテストのみ再実行
uv run pytest --lf

# 並列実行（pytest-xdistが必要）
uv run pytest -n auto
```

カバレッジレポートは `htmlcov/index.html` で確認できます。

### フロントエンドテスト

```bash
cd frontend

# すべてのテストを実行
npm test

# カバレッジ付きで実行
npm run test:coverage

# ウォッチモードで実行（ファイル変更を監視）
npm run test:watch

# UIモードで実行
npm run test:ui

# 特定のテストファイルを実行
npm test src/components/Button.test.tsx
```

### E2Eテスト

```bash
cd frontend

# E2Eテストの実行
npm run test:e2e

# ヘッドレスモードで実行
npm run test:e2e -- --headless
```

### Dockerでのテスト実行

```bash
# バックエンドテスト
docker compose exec backend pytest

# フロントエンドテスト
docker compose exec frontend npm test
```

## コード品質チェック

### バックエンド

```bash
cd backend

# Lint チェック
uv run ruff check .

# Lint 自動修正
uv run ruff check --fix .

# フォーマット
uv run ruff format .

# 型チェック
uv run pyright

# すべてのチェックを一度に実行
uv run ruff check . && uv run ruff format . && uv run pyright

# pre-commit フック（コミット前チェック）
pre-commit run --all-files
```

### フロントエンド

```bash
cd frontend

# Lint チェック
npm run lint

# Lint 自動修正
npm run lint:fix

# フォーマット
npm run format

# 型チェック
npm run build  # TypeScriptのビルド時に型チェックが実行されます
```

## データベース操作

### マイグレーション

```bash
cd backend

# マイグレーションファイルの作成
uv run python manage.py makemigrations

# マイグレーションの適用
uv run python manage.py migrate

# 特定のアプリのマイグレーション
uv run python manage.py makemigrations api
uv run python manage.py migrate api

# マイグレーション状況の確認
uv run python manage.py showmigrations

# マイグレーションの取り消し（特定のマイグレーションまで戻す）
uv run python manage.py migrate api 0001_initial

# SQLの確認（実行せずにSQL文を表示）
uv run python manage.py sqlmigrate api 0001
```

### データベースのリセット

```bash
cd backend

# データベースファイルの削除
rm db.sqlite3

# マイグレーションの再実行
uv run python manage.py migrate

# スーパーユーザーの再作成
uv run python manage.py createsuperuser
```

### データのインポート/エクスポート

```bash
cd backend

# データのエクスポート（全体）
uv run python manage.py dumpdata > data.json

# 特定のアプリのデータをエクスポート
uv run python manage.py dumpdata api > api_data.json

# データのインポート
uv run python manage.py loaddata data.json

# インデント付きでエクスポート（可読性向上）
uv run python manage.py dumpdata --indent 2 > data.json
```

## 便利なコマンド

### Djangoシェル

```bash
cd backend

# Pythonシェル（Django設定込み）
uv run python manage.py shell

# IPythonシェル（より使いやすい）
uv run python manage.py shell
```

シェル内での操作例:
```python
# モデルのインポート
from api.models import Board, Thread, Post

# データの作成
board = Board.objects.create(name="テスト板", slug="test")

# データの取得
boards = Board.objects.all()
board = Board.objects.get(slug="test")

# データの更新
board.name = "新しい名前"
board.save()

# データの削除
board.delete()
```

### 静的ファイルの収集

```bash
cd backend

# 静的ファイルを STATIC_ROOT にコピー
uv run python manage.py collectstatic

# 確認なしで実行
uv run python manage.py collectstatic --noinput
```

### カスタム管理コマンド

プロジェクト固有の管理コマンドを実行:

```bash
cd backend

# 利用可能なコマンドの確認
uv run python manage.py help

# 例: サンプルデータの生成
uv run python manage.py create_sample_data
```

## 環境変数

### バックエンド環境変数

`.env.example` ファイルをコピーして `.env` を作成します：

```bash
cd backend
cp .env.example .env
```

主要な環境変数:

```env
# Django設定
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# データベース（本番環境用）
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# CORS設定
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Wagtail管理画面
WAGTAIL_SITE_NAME=Modern Board
```

**重要**:
- 開発環境では `DJANGO_DEBUG=True` を設定
- 本番環境では必ず強力な `DJANGO_SECRET_KEY` を生成して使用
- 本番環境では `DJANGO_DEBUG=False` に設定

### フロントエンド環境変数

```bash
cd frontend
cp .env.example .env
```

主要な環境変数:

```env
# API エンドポイント
VITE_API_URL=http://localhost:8000/api/v1

# 環境
VITE_ENV=development
```

## デバッグ方法

### バックエンドデバッグ

#### pdb を使用したデバッグ

コード内に以下を追加:
```python
import pdb; pdb.set_trace()
```

よく使うpdbコマンド:
- `n` (next): 次の行へ
- `s` (step): 関数の中に入る
- `c` (continue): 次のブレークポイントまで実行
- `l` (list): 現在の位置のコードを表示
- `p variable_name`: 変数の値を表示
- `q` (quit): デバッガを終了

#### VSCode デバッグ設定

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django: Backend",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/backend/manage.py",
      "args": ["runserver"],
      "django": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

#### ログの確認

```python
import logging

logger = logging.getLogger(__name__)

# ログ出力
logger.debug("デバッグ情報")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
```

### フロントエンドデバッグ

#### ブラウザ開発者ツール

1. Chrome DevTools を開く（F12 または Cmd+Option+I）
2. Console タブでログを確認
3. Sources タブでブレークポイントを設定
4. Network タブでAPI通信を確認

#### console.log によるデバッグ

```typescript
console.log('値の確認:', variable);
console.error('エラー:', error);
console.table(arrayData);  // 配列をテーブル形式で表示
console.dir(object);  // オブジェクトの詳細を表示
```

#### VSCode デバッグ設定

`.vscode/launch.json` に追加:
```json
{
  "name": "Chrome: Frontend",
  "type": "chrome",
  "request": "launch",
  "url": "http://localhost:5173",
  "webRoot": "${workspaceFolder}/frontend/src"
}
```

#### React Developer Tools

[React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi) をインストールして、コンポーネントの状態を確認できます。

## トラブルシューティング

### ポートが既に使用されている

#### バックエンド（ポート8000）

```bash
# ポートを使用しているプロセスを確認
lsof -i :8000

# プロセスを終了
kill -9 <PID>

# または別のポートで起動
uv run python manage.py runserver 8080
```

#### フロントエンド（ポート5173）

```bash
# ポートを使用しているプロセスを確認
lsof -i :5173

# プロセスを終了
kill -9 <PID>

# または別のポートで起動
npm run dev -- --port 3000
```

### データベース接続エラー

```bash
# マイグレーションの状態を確認
cd backend
uv run python manage.py showmigrations

# マイグレーションを再実行
uv run python manage.py migrate

# データベースをリセット（注意: すべてのデータが削除されます）
rm db.sqlite3
uv run python manage.py migrate
```

### npm install エラー

```bash
cd frontend

# キャッシュをクリア
npm cache clean --force

# node_modules を削除して再インストール
rm -rf node_modules package-lock.json
npm install
```

### Docker関連のエラー

```bash
# コンテナとボリュームを削除して再構築
docker compose down -v
docker compose build --no-cache
docker compose up -d

# ログを確認
docker compose logs -f

# コンテナに入って確認
docker compose exec backend bash
docker compose exec frontend sh
```

### Python仮想環境のエラー

```bash
cd backend

# 仮想環境を削除
rm -rf .venv

# 再作成
uv sync --extra dev
```

### マイグレーションの競合

```bash
cd backend

# 競合を確認
uv run python manage.py showmigrations

# マイグレーションファイルを削除して再作成
rm api/migrations/00*.py
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### キャッシュのクリア

```bash
# Pythonキャッシュのクリア
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# npm キャッシュのクリア
cd frontend
npm cache clean --force
rm -rf node_modules/.cache
```

## パフォーマンス最適化

### Django Debug Toolbar（開発環境）

開発環境でSQLクエリやパフォーマンスを確認:

```bash
cd backend
uv pip install django-debug-toolbar
```

`config/settings/dev.py` に設定を追加:
```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

### フロントエンドビルドの最適化

```bash
cd frontend

# 本番ビルド
npm run build

# ビルドサイズの確認
npm run build -- --mode production

# ビルド結果のプレビュー
npm run preview
```

## 次のステップ

- [CONTRIBUTING.md](./CONTRIBUTING.md) - コントリビューション方法
- [タスク管理](./tasks/README.md) - 開発タスクの確認
- [DOCKER.md](../DOCKER.md) - Docker詳細ガイド

## サポート

問題が解決しない場合は、以下をお試しください:

1. [GitHub Issues](https://github.com/kkm-horikawa/modern-board/issues) を検索
2. 新しい Issue を作成（エラーメッセージと環境情報を含める）
3. プロジェクトメンバーに相談
