# 📋 Modern Board - プロジェクト初期セットアップ定義

このファイルは、Modern Boardプロジェクトの初期セットアップに使用されます。
Claudeが最初の実行時にこのファイルを読み取り、プロジェクト・マイルストーン・初期Issueを作成します。

---

## 🎯 プロジェクト情報

**プロジェクト名**: Modern Board
**説明**: 掲示板アプリケーション - React + FastAPI + PostgreSQL

**プロジェクトの目的**:
- モダンな技術スタックを使用した掲示板アプリケーションの開発
- フロントエンド（React + TypeScript）とバックエンド（FastAPI + Python）の実装
- Docker Composeを使用したローカル開発環境
- Claude完全自律開発システムの実証プロジェクト

**技術スタック**:
- Frontend: React, TypeScript, Vite
- Backend: FastAPI, Python, SQLAlchemy
- Database: PostgreSQL
- Infrastructure: Docker, Docker Compose
- CI/CD: GitHub Actions

---

## 📅 マイルストーン定義

### マイルストーン0: 自動化基盤構築
**説明**: Claude完全自律開発システムの構築と動作確認

**初期Issue:**
- GitHub Actions ワークフローのセットアップ
  - labels: `setup`, `priority:critical`, `infrastructure`
  - 説明: claude-project-manager.yml、claude.yml、Slack通知の設定

- プロジェクト管理テンプレートの作成
  - labels: `setup`, `priority:high`, `documentation`
  - 説明: project-management-issue.mdなどのテンプレート作成

- 初回定期実行の動作確認
  - labels: `setup`, `priority:high`, `testing`
  - 説明: 30分おきの定期実行が正しく動作するか確認

### マイルストーン1: MVP - ローカル動作確認
**説明**: 最小限の機能を持つ掲示板アプリのローカル動作確認

**初期Issue:**
- FE-001: フロントエンドプロジェクトのセットアップ
  - labels: `setup`, `priority:high`, `frontend`
  - 説明: React + TypeScript + Vite のセットアップ、アーキテクチャ設計

- BE-001: バックエンドプロジェクトのセットアップ
  - labels: `setup`, `priority:high`, `backend`
  - 説明: FastAPI + SQLAlchemy のセットアップ、アーキテクチャ設計

- DB-001: データベーススキーマ設計
  - labels: `database`, `priority:high`, `design`
  - 説明: PostgreSQLスキーマ設計、マイグレーション設定

- INFRA-001: Docker Compose環境構築
  - labels: `infrastructure`, `priority:high`, `setup`
  - 説明: フロントエンド、バックエンド、データベースのDocker Compose設定

- FE-002: スレッド一覧表示機能
  - labels: `feature`, `priority:high`, `frontend`
  - 説明: スレッド一覧を表示するUIの実装

- BE-002: スレッドAPI実装
  - labels: `feature`, `priority:high`, `backend`
  - 説明: スレッドのCRUD APIエンドポイント実装

- FE-003: スレッド詳細・コメント表示
  - labels: `feature`, `priority:high`, `frontend`
  - 説明: スレッド詳細とコメント一覧の表示

- BE-003: コメントAPI実装
  - labels: `feature`, `priority:high`, `backend`
  - 説明: コメントのCRUD APIエンドポイント実装

### マイルストーン2: フル機能実装
**説明**: 掲示板として必要な全機能の実装

**初期Issue:**
- FE-004: 画像アップロード機能
  - labels: `feature`, `priority:medium`, `frontend`
  - 説明: コメントへの画像添付機能のUI実装

- BE-004: 画像アップロードAPI
  - labels: `feature`, `priority:medium`, `backend`
  - 説明: 画像アップロード・保存・配信のAPI実装

- FE-005: 検索機能
  - labels: `feature`, `priority:medium`, `frontend`
  - 説明: スレッド・コメントの検索UI実装

- BE-005: 検索API
  - labels: `feature`, `priority:medium`, `backend`
  - 説明: 全文検索APIの実装

- FE-006: ページネーション
  - labels: `enhancement`, `priority:medium`, `frontend`
  - 説明: スレッド一覧・コメント一覧のページネーション

- TEST-001: フロントエンドテスト実装
  - labels: `testing`, `priority:high`, `frontend`
  - 説明: Vitestを使用したユニットテスト・統合テストの実装

- TEST-002: バックエンドテスト実装
  - labels: `testing`, `priority:high`, `backend`
  - 説明: pytestを使用したユニットテスト・統合テストの実装

- DOC-001: API仕様書作成
  - labels: `documentation`, `priority:medium`
  - 説明: OpenAPI/Swaggerを使用したAPI仕様書の作成

### マイルストーン3: デプロイと公開
**説明**: プロダクション環境へのデプロイと公開

**初期Issue:**
- DEPLOY-001: デプロイ戦略の策定
  - labels: `deployment`, `priority:high`, `design`
  - 説明: デプロイ先の選定、環境構成、CI/CDパイプライン設計

- DEPLOY-002: プロダクション環境構築
  - labels: `deployment`, `priority:high`, `infrastructure`
  - 説明: 本番環境のセットアップ、環境変数管理

- DEPLOY-003: デプロイ自動化
  - labels: `deployment`, `priority:high`, `infrastructure`
  - 説明: GitHub ActionsでのデプロイCI/CD構築

- SECURITY-001: セキュリティ対策
  - labels: `security`, `priority:critical`
  - 説明: CORS、CSRF、SQLインジェクション対策など

- DOC-002: ユーザードキュメント作成
  - labels: `documentation`, `priority:medium`
  - 説明: エンドユーザー向けの使い方ガイド作成

### マイルストーン4: 運用とメンテナンス
**説明**: 運用開始後の監視、改善、機能追加

**初期Issue:**
- MONITOR-001: 監視システム構築
  - labels: `infrastructure`, `priority:high`, `monitoring`
  - 説明: ログ収集、メトリクス監視、アラート設定

- PERF-001: パフォーマンス最適化
  - labels: `enhancement`, `priority:medium`, `performance`
  - 説明: フロントエンド・バックエンドのパフォーマンス改善

- DOC-003: 運用マニュアル作成
  - labels: `documentation`, `priority:medium`
  - 説明: 運用担当者向けのトラブルシューティングガイド

---

## 🏷️ 推奨ラベル

プロジェクトで使用する標準ラベル（Claudeが自動作成）:

**優先度:**
- `priority:critical` - 最優先で対応が必要
- `priority:high` - 高優先度
- `priority:medium` - 中優先度
- `priority:low` - 低優先度

**カテゴリ:**
- `bug` - バグ修正
- `feature` - 新機能
- `enhancement` - 既存機能の改善
- `documentation` - ドキュメント
- `testing` - テスト関連
- `infrastructure` - インフラ・CI/CD
- `design` - 設計・アーキテクチャ
- `setup` - セットアップ関連
- `deployment` - デプロイ関連
- `database` - データベース関連
- `security` - セキュリティ関連
- `performance` - パフォーマンス関連
- `monitoring` - 監視関連

**技術スタック:**
- `frontend` - フロントエンド関連
- `backend` - バックエンド関連

**プロジェクト管理:**
- `project-management` - プロジェクト管理関連
- `automated` - 自動化タスク

---

## 📝 注意事項

このファイルは Modern Board プロジェクト専用の設定です。
テンプレートリポジトリから新規プロジェクトを作成する場合は、
`.github/templates/project-setup.md` を自分のプロジェクトに合わせてカスタマイズしてください。
