# FE-002: 共通コンポーネントライブラリの構築（親タスク）

## 概要
再利用可能な共通コンポーネントを作成し、一貫性のあるUIを提供する。

**注**: このタスクは大きいため、以下のサブタスクに分割されています。各サブタスクを個別のPRとして実装してください。

## サブタスク
- **FE-002-1**: Layoutコンポーネントの実装
- **FE-002-2**: 基本UIコンポーネントの実装
- **FE-002-3**: 掲示板特化コンポーネントの実装
- **FE-002-4**: フォームコンポーネントの実装

## 優先度
**High** - 他のフロントエンドタスクの基盤

## 難易度
**Medium** (全体として)

## 前提条件
- [x] FE-001: プロジェクトセットアップが完了している
- [ ] UIフレームワークの選定が完了している
- [ ] デザインシステムの方針が決まっている

## 実装内容

### 1. Layoutコンポーネント (`src/components/layout/`)
- [ ] `Header` - ヘッダー（タイトル、ナビゲーション）
- [ ] `Footer` - フッター
- [ ] `Sidebar` - サイドバー（カテゴリ一覧等）
- [ ] `Container` - コンテンツコンテナ
- [ ] `MainLayout` - メインレイアウト（Header + Content + Footer）

### 2. 基本UIコンポーネント (`src/components/common/`)
- [ ] `Button` - ボタン（Primary, Secondary, Danger等）
- [ ] `Input` - テキスト入力
- [ ] `Textarea` - 複数行テキスト入力
- [ ] `Select` - セレクトボックス
- [ ] `Checkbox` - チェックボックス
- [ ] `Radio` - ラジオボタン
- [ ] `Label` - ラベル
- [ ] `ErrorMessage` - エラーメッセージ表示
- [ ] `Spinner` - ローディングインジケーター
- [ ] `Modal` - モーダルダイアログ
- [ ] `Tooltip` - ツールチップ
- [ ] `Badge` - バッジ（NEW、HOT等）
- [ ] `Divider` - 区切り線
- [ ] `Card` - カード

### 3. 掲示板特化コンポーネント (`src/components/features/`)
- [ ] `ThreadCard` - スレッドカード（一覧表示用）
- [ ] `PostItem` - 投稿アイテム
- [ ] `ReactionButton` - リアクションボタン
- [ ] `CategoryBadge` - カテゴリバッジ
- [ ] `TagChip` - タグチップ
- [ ] `TrendingIndicator` - トレンド表示
- [ ] `PinnedIndicator` - ピン留め表示
- [ ] `LockedIndicator` - ロック表示
- [ ] `Pagination` - ページネーション
- [ ] `SortSelector` - ソート選択
- [ ] `FilterPanel` - フィルタパネル

### 4. フォームコンポーネント (`src/components/forms/`)
- [ ] `ThreadCreateForm` - スレッド作成フォーム
- [ ] `PostCreateForm` - 投稿作成フォーム
- [ ] `FormField` - フォームフィールドラッパー（ラベル+入力+エラー）
- [ ] `FormGroup` - フォームグループ

### 5. ナビゲーションコンポーネント (`src/components/navigation/`)
- [ ] `Breadcrumb` - パンくずリスト
- [ ] `NavMenu` - ナビゲーションメニュー
- [ ] `TabMenu` - タブメニュー

### 6. TypeScript型定義
- [ ] 各コンポーネントのPropsインターフェース定義
- [ ] イベントハンドラの型定義
- [ ] 共通型の抽出（Size, Variant等）

### 7. アクセシビリティ対応
- [ ] ARIA属性の適切な設定
- [ ] キーボードナビゲーション対応
- [ ] フォーカス管理
- [ ] スクリーンリーダー対応

### 8. テスト
- [ ] 各コンポーネントのユニットテスト（Vitest）
- [ ] スナップショットテスト
- [ ] アクセシビリティテスト（jest-axe）

### 9. ドキュメント（オプション）
- [ ] Storybookストーリーの作成
- [ ] 使用例のドキュメント
- [ ] PropTypes/インターフェースのドキュメント

## 受け入れ基準
- [ ] すべての共通コンポーネントが実装されている
- [ ] TypeScript型定義が完備されている
- [ ] レスポンシブデザインに対応している
- [ ] アクセシビリティ基準を満たしている
- [ ] テストカバレッジ80%以上
- [ ] 再利用可能で拡張性がある
- [ ] スタイルが統一されている
- [ ] パフォーマンスが良好（不要な再レンダリングなし）

## コンポーネント設計原則
- **Single Responsibility**: 1つのコンポーネントは1つの責任のみ
- **Composition over Inheritance**: 継承より合成を優先
- **Props Driven**: Propsで振る舞いを制御
- **Accessible by Default**: デフォルトでアクセシブル
- **Type Safe**: 型安全性を確保
- **Testable**: テスト可能な設計

## 関連タスク
- FE-001: プロジェクトセットアップ
- FE-003: スレッド一覧ページ実装
- FE-004: スレッド詳細ページ実装
- FE-006: レスポンシブデザイン対応

## 参考
- React Component Patterns: https://www.patterns.dev/react
- Accessible Components: https://www.a11y-101.com/
- Component Testing: https://testing-library.com/react
