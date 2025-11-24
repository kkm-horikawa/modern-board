# 📋 プロジェクト初期セットアップ定義

このファイルは、テンプレートリポジトリから作成した新規プロジェクトの初期セットアップに使用されます。
Claudeが最初の実行時にこのファイルを読み取り、プロジェクト・マイルストーン・初期Issueを自動作成します。

**重要**: このファイルをあなたのプロジェクトに合わせてカスタマイズしてください。

---

## 🎯 プロジェクト情報

**プロジェクト名**: My Awesome Project
**説明**: 簡潔なプロジェクトの説明をここに記載してください

**プロジェクトの目的**:
- このプロジェクトで達成したい主な目標
- ターゲットユーザーや使用シーン
- 技術スタック（例: React, FastAPI, PostgreSQL）

---

## 📅 マイルストーン定義

### マイルストーン1: プロジェクト基盤構築
**説明**: プロジェクトの基盤となる構造とツールチェーンを構築

**初期Issue:**
- プロジェクト構造のセットアップ
  - labels: `setup`, `priority:high`
  - 説明: リポジトリ構造、ディレクトリ構成、基本的な設定ファイルの作成

- CI/CDパイプラインの構築
  - labels: `infrastructure`, `priority:high`
  - 説明: GitHub Actions、テスト自動化、リンター設定

- 開発環境のセットアップドキュメント
  - labels: `documentation`, `priority:medium`
  - 説明: README、CONTRIBUTING、開発者向けドキュメントの作成

### マイルストーン2: コア機能実装
**説明**: プロジェクトの主要機能を実装

**初期Issue:**
- 機能設計ドキュメントの作成
  - labels: `design`, `priority:high`
  - 説明: 主要機能の設計書、アーキテクチャ図の作成

- データモデル/スキーマ設計
  - labels: `database`, `priority:high`
  - 説明: データベーススキーマ、APIスキーマの設計

- 基本的なCRUD操作の実装
  - labels: `feature`, `priority:high`
  - 説明: 基本的なCreate/Read/Update/Delete操作の実装

### マイルストーン3: 追加機能とテスト
**説明**: 追加機能の実装とテストカバレッジの向上

**初期Issue:**
- ユニットテストの実装
  - labels: `testing`, `priority:high`
  - 説明: コア機能のユニットテストを実装

- 統合テストの実装
  - labels: `testing`, `priority:medium`
  - 説明: APIやコンポーネント間の統合テストを実装

- エラーハンドリングとバリデーション
  - labels: `enhancement`, `priority:medium`
  - 説明: エラーハンドリング、入力バリデーションの強化

### マイルストーン4: デプロイと公開
**説明**: プロダクション環境へのデプロイと公開準備

**初期Issue:**
- デプロイ戦略の策定
  - labels: `deployment`, `priority:high`
  - 説明: デプロイ方法、環境構成、ロールバック戦略の策定

- プロダクション環境のセットアップ
  - labels: `infrastructure`, `priority:high`
  - 説明: 本番環境の構築、監視設定

- ユーザードキュメントの作成
  - labels: `documentation`, `priority:medium`
  - 説明: エンドユーザー向けのドキュメント、チュートリアル作成

---

## 🏷️ 推奨ラベル

プロジェクトで使用する標準ラベル（Claudeが自動作成）:

- `priority:critical` - 最優先で対応が必要
- `priority:high` - 高優先度
- `priority:medium` - 中優先度
- `priority:low` - 低優先度
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

---

## 📝 カスタマイズ方法

1. **プロジェクト情報**: あなたのプロジェクトに合わせて名前・説明を変更
2. **マイルストーン**: 必要に応じてマイルストーンを追加/削除/変更
3. **初期Issue**: 各マイルストーンの初期Issueをカスタマイズ
4. **ラベル**: プロジェクトに必要なラベルを追加

カスタマイズ後、最初の `claude-project-manager.yml` 実行時に自動セットアップされます。