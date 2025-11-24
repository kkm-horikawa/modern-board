# Modern Board - タスク管理

このディレクトリには、Modern Board（匿名掲示板アプリケーション）の開発タスクが含まれています。各タスクは個別のMarkdownファイルとして管理され、複数人での並行開発を可能にします。

## 📁 ディレクトリ構成

```
docs/tasks/
├── README.md               # このファイル
├── backend/                # バックエンド関連タスク
│   ├── BE-001-api-integration-tests.md
│   ├── BE-002-authentication-authorization.md
│   ├── BE-003-spam-prevention-rate-limiting.md
│   └── BE-004-redis-caching.md
├── frontend/               # フロントエンド関連タスク
│   ├── FE-001-project-setup-architecture.md
│   ├── FE-002-component-library.md
│   ├── FE-003-thread-list-page.md
│   └── FE-004-thread-detail-page.md
├── infrastructure/         # インフラ・デプロイ関連タスク
│   ├── INF-001-docker-compose-production.md
│   └── INF-002-cicd-pipeline.md
├── integration/            # 統合テスト関連タスク
│   └── INT-001-e2e-testing.md
└── documentation/          # ドキュメント関連タスク
```

## 🏷️ タスクID命名規則

- **BE-XXX**: Backend（バックエンド）
- **FE-XXX**: Frontend（フロントエンド）
- **INF-XXX**: Infrastructure（インフラ）
- **INT-XXX**: Integration（統合）
- **DOC-XXX**: Documentation（ドキュメント）

## 📊 優先度の定義

各タスクには優先度が設定されています：

- **High**: プロジェクトのコア機能に必要、MVP（最小実用製品）に含まれる
- **Medium**: 重要だが初期リリースには必須ではない
- **Low**: あると良い機能、将来的な改善項目

## 🎯 難易度の定義

- **Easy**: 1-2日で完了可能、基本的な知識で対応可能
- **Medium**: 3-5日で完了可能、中級レベルの知識が必要
- **Hard**: 1週間以上、高度な知識や設計が必要

## 🚀 推奨実装順序

### フェーズ1: MVP開発（High優先度）

#### バックエンド
1. ✅ **完了済み**: モデル実装、シリアライザ、ViewSet、APIドキュメント
2. ✅ **完了済み**: モデルテスト（99%カバレッジ）
3. **BE-001**: API統合テストの実装
4. **BE-002**: 認証・認可システムの実装

#### フロントエンド
1. **FE-001**: プロジェクトセットアップとアーキテクチャ設計
2. **FE-002**: 共通コンポーネントライブラリの構築
3. **FE-003**: スレッド一覧ページの実装
4. **FE-004**: スレッド詳細・投稿一覧ページの実装

### フェーズ2: 機能拡張とパフォーマンス（Medium優先度）

#### バックエンド
5. **BE-003**: スパム対策・レート制限の実装

#### フロントエンド
6. スレッド作成フォームの実装
7. レスポンシブデザイン対応
8. フロントエンドテストの実装

#### 統合
9. **INT-001**: E2Eテストの実装

### フェーズ3: 本番環境準備（Medium優先度）

#### インフラ
10. **INF-001**: 本番用Docker Compose設定
11. **INF-002**: CI/CDパイプラインの構築
12. 本番環境へのデプロイ

### フェーズ4: 最適化と改善（Low優先度）

13. **BE-004**: Redisキャッシュの導入
14. パフォーマンステストと最適化
15. セキュリティ監査と改善
16. ドキュメントの充実

## 📝 タスクフォーマット

各タスクファイルには以下の情報が含まれています：

```markdown
# タスクID: タスク名

## 概要
タスクの説明

## 優先度
High / Medium / Low

## 難易度
Easy / Medium / Hard

## 前提条件
- 依存するタスクや準備事項

## 実装内容
- 具体的な実装項目（チェックリスト形式）

## 受け入れ基準
- タスク完了の判断基準

## 関連タスク
- 関連するタスクのリスト

## 参考
- 参考資料へのリンク
```

## 🔄 タスクの進行管理

### タスクの選択方法

1. **優先度の確認**: High → Medium → Low の順に着手
2. **前提条件の確認**: 依存するタスクが完了しているか確認
3. **スキルマッチング**: 自分のスキルセットに合ったタスクを選択
4. **並行作業の調整**: 他のメンバーと重複しないよう調整

### タスクの進め方

1. タスクファイルを読み、実装内容を理解する
2. 実装内容のチェックリストに従って作業を進める
3. 受け入れ基準を満たしているか確認する
4. テストを実行し、すべてパスすることを確認する
5. コードレビューを依頼する
6. マージ後、関連タスクを更新する

### ブランチ戦略

```bash
# 機能ブランチの命名規則
feature/BE-001-api-integration-tests
feature/FE-003-thread-list-page

# ブランチ作成例
git checkout -b feature/BE-001-api-integration-tests
```

## 📈 進捗の可視化

GitHub Projectsまたは類似のツールを使用して、タスクの進捗を可視化することを推奨します：

- **Todo**: 未着手
- **In Progress**: 作業中
- **Review**: レビュー待ち
- **Done**: 完了

## 🛠️ 技術スタック（参考）

### バックエンド
- Python 3.13
- Django 5.2+
- Django REST Framework 3.16+
- Wagtail 7.2+
- PostgreSQL 16
- Redis 7
- pytest, pytest-django, pytest-cov
- Ruff（リンター）
- Pyright（型チェッカー）

### フロントエンド
- React 19.2
- TypeScript 5.9
- Vite 7.1
- TanStack Query（推奨）
- Zustand または Jotai（状態管理、推奨）
- shadcn/ui + Tailwind CSS（推奨）
- Vitest（テスト）
- Playwright（E2Eテスト）

### インフラ
- Docker & Docker Compose
- GitHub Actions（CI/CD）
- Nginx（リバースプロキシ）
- Gunicorn（WSGIサーバー）

## 📚 追加リソース

- [開発ガイドライン](../DEVELOPMENT.md)（作成予定）
- [APIドキュメント](http://localhost:8000/api/schema/swagger-ui/)（開発環境）
- [テストガイド](https://refrainit.com/list/testing-guide-python-typescript/)
- [コーディング規約](../CODING_STANDARDS.md)（作成予定）

## 🤝 貢献方法

1. タスクを選択し、自分に割り当てる
2. 機能ブランチを作成する
3. 実装とテストを行う
4. プルリクエストを作成する
5. コードレビューを受ける
6. マージ後、タスクを完了としてマークする

## ❓ 質問・相談

- 技術的な質問: GitHub Discussionsまたはチームチャット
- タスクの優先度変更: プロジェクトマネージャーに相談
- 新しいタスクの追加: 提案を議論してから追加

---

**最終更新日**: 2025-11-24
**ドキュメントバージョン**: 1.0
