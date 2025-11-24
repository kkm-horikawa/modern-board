# BE-001: API統合テストの実装

## 概要
バックエンドAPIエンドポイントの統合テストを実装し、実際のHTTPリクエスト/レスポンスの動作を検証する。

## 優先度
**High** - コア機能の品質保証に必要

## 難易度
**Medium**

## 前提条件
- [x] モデルテストが完成している（99%カバレッジ達成済み）
- [x] ViewSetとSerializerが実装済み
- [x] pytest-djangoとDRF TestCaseが利用可能

## 実装内容

### 1. カテゴリAPI統合テスト (`api/tests/integration/test_categories_api.py`)
- [ ] カテゴリ一覧取得APIのテスト
- [ ] カテゴリ詳細取得APIのテスト
- [ ] カテゴリ作成APIのテスト（認証が必要な場合）
- [ ] カテゴリ更新APIのテスト
- [ ] カテゴリ削除APIのテスト
- [ ] スレッド数の集計が正しいことを確認

### 2. タグAPI統合テスト (`api/tests/integration/test_tags_api.py`)
- [ ] タグ一覧取得APIのテスト
- [ ] タグ詳細取得APIのテスト
- [ ] タグ作成APIのテスト
- [ ] タグ更新APIのテスト
- [ ] タグ削除APIのテスト

### 3. スレッドAPI統合テスト (`api/tests/integration/test_threads_api.py`)
- [ ] スレッド一覧取得APIのテスト（フィルタ、ソート含む）
- [ ] スレッド詳細取得APIのテスト
- [ ] スレッド作成APIのテスト（初回投稿含む）
- [ ] スレッド更新APIのテスト
- [ ] スレッドピン留めAPIのテスト
- [ ] スレッドロックAPIのテスト
- [ ] トレンドスレッド取得APIのテスト
- [ ] 閲覧数インクリメントの動作確認

### 4. 投稿API統合テスト (`api/tests/integration/test_posts_api.py`)
- [ ] 投稿一覧取得APIのテスト
- [ ] 投稿詳細取得APIのテスト
- [ ] 投稿作成APIのテスト（post_number自動採番確認）
- [ ] 投稿更新APIのテスト
- [ ] 投稿削除APIのテスト
- [ ] リアクション追加APIのテスト
- [ ] リアクション集計の確認

### 5. 統計API統合テスト (`api/tests/integration/test_stats_api.py`)
- [ ] ボード統計取得APIのテスト
- [ ] トレンドスレッド取得APIのテスト
- [ ] トップユーザー取得APIのテスト
- [ ] アクティビティフィード取得APIのテスト

### 6. テスト環境整備
- [ ] `api/tests/integration/`ディレクトリ作成
- [ ] `conftest.py`で共通フィクスチャを定義
- [ ] APIClientのセットアップ
- [ ] テストデータファクトリの作成（必要に応じて）

## 受け入れ基準
- [ ] すべてのAPI統合テストがパスする
- [ ] テストカバレッジ90%以上を維持
- [ ] HTTPステータスコードが正しく返される
- [ ] レスポンスのJSONスキーマが正しい
- [ ] エッジケース（存在しないID、バリデーションエラー等）をカバー
- [ ] pytest実行時間が妥当な範囲（全体で30秒以内目安）

## 関連タスク
- BE-002: 認証・認可システムの実装（認証が必要なエンドポイントのテストに影響）
- BE-005: APIパフォーマンステスト

## 参考
- Testing guide: https://refrainit.com/list/testing-guide-python-typescript/
- DRF Testing: https://www.django-rest-framework.org/api-guide/testing/
