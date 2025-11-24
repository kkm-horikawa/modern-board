# FE-001: フロントエンドプロジェクトのセットアップとアーキテクチャ設計

## 概要
React 19.2 + TypeScript 5.9 + Vite 7.1 を使用したフロントエンドプロジェクトの初期セットアップとアーキテクチャを確立する。

## 優先度
**High** - フロントエンド開発の基盤

## 難易度
**Medium**

## 前提条件
- [x] Vite 7.1がセットアップ済み（`frontend`ディレクトリ）
- [x] React 19.2とTypeScript 5.9がインストール済み
- [ ] バックエンドAPIエンドポイントが利用可能

## 実装内容

### 1. プロジェクト構造の確立
```
frontend/
├── src/
│   ├── components/      # 再利用可能なコンポーネント
│   │   ├── common/      # ボタン、入力フィールド等
│   │   ├── layout/      # ヘッダー、フッター、サイドバー
│   │   └── features/    # 機能別コンポーネント
│   ├── pages/           # ページコンポーネント
│   ├── hooks/           # カスタムフック
│   ├── services/        # API通信
│   ├── stores/          # 状態管理（Zustand推奨）
│   ├── types/           # TypeScript型定義
│   ├── utils/           # ユーティリティ関数
│   ├── constants/       # 定数定義
│   └── styles/          # グローバルスタイル
```

### 2. 必要なライブラリのインストールと設定
- [ ] ルーティング: React Router v6
- [ ] 状態管理: Zustand または Jotai（軽量を優先）
- [ ] HTTP クライアント: axios または TanStack Query
- [ ] UI フレームワーク: 決定が必要（以下から選択）
  - [ ] shadcn/ui + Tailwind CSS（推奨）
  - [ ] MUI (Material-UI)
  - [ ] Mantine
- [ ] フォーム管理: React Hook Form
- [ ] バリデーション: Zod
- [ ] 日時処理: date-fns
- [ ] コードフォーマット: Prettier（設定済みか確認）
- [ ] リンター: ESLint（設定済みか確認）

### 3. TypeScript設定の最適化
- [ ] 厳格モードの有効化
- [ ] パスエイリアス設定（`@/`等）
- [ ] 型定義ファイルの整理
- [ ] APIレスポンス型の自動生成検討（OpenAPI Generator）

### 4. API通信層のセットアップ
- [ ] axios インスタンスの作成
- [ ] ベースURL設定（環境変数）
- [ ] リクエスト/レスポンスインターセプター
- [ ] エラーハンドリング
- [ ] 型安全なAPIクライアント作成

### 5. 状態管理アーキテクチャ
- [ ] グローバルステートの設計
- [ ] ローカルステートのパターン確立
- [ ] サーバーステート管理（TanStack Query推奨）
- [ ] キャッシュ戦略の決定

### 6. ルーティング設計
- [ ] ページ構成の決定
  - `/` - トップページ（スレッド一覧）
  - `/categories/:id` - カテゴリ別スレッド一覧
  - `/threads/:id` - スレッド詳細（投稿一覧）
  - `/create-thread` - スレッド作成
  - その他必要なページ
- [ ] Lazy loadingの設定
- [ ] 404ページの実装

### 7. スタイリング戦略
- [ ] Tailwind CSS設定（推奨の場合）
- [ ] CSS Modulesまたは CSS-in-JS の選択
- [ ] レスポンシブデザインのブレークポイント定義
- [ ] カラーパレット・テーマの設定
- [ ] ダークモード対応（オプション）

### 8. 開発ツール設定
- [ ] ESLintルールのカスタマイズ
- [ ] Prettierフォーマット設定
- [ ] Vitestのセットアップ（テスト）
- [ ] Storybookのセットアップ（オプション）
- [ ] pre-commitフックの設定

## 受け入れ基準
- [ ] プロジェクト構造が確立されている
- [ ] 必要なライブラリがインストール済み
- [ ] TypeScript設定が最適化されている
- [ ] API通信の基本実装が完了している
- [ ] ルーティングが動作している
- [ ] スタイリングシステムが機能している
- [ ] ビルドとdevサーバーが正常に動作する
- [ ] 型チェックでエラーが出ない

## 技術的決定事項（要確認）
- [ ] 状態管理ライブラリの選定（Zustand vs Jotai vs Redux Toolkit）
- [ ] UIフレームワークの選定（shadcn/ui vs MUI vs Mantine）
- [ ] CSS戦略（Tailwind vs CSS Modules vs CSS-in-JS）
- [ ] データフェッチング戦略（TanStack Query vs SWR vs 素のaxios）

## 関連タスク
- FE-002: コンポーネントライブラリの構築
- FE-003: スレッド一覧ページの実装
- FE-004: スレッド詳細ページの実装
- BE-001: API統合テスト（API仕様の確認）

## 参考
- React 19: https://react.dev/
- Vite: https://vite.dev/
- React Router: https://reactrouter.com/
- TanStack Query: https://tanstack.com/query/
- Zustand: https://zustand-demo.pmnd.rs/
- shadcn/ui: https://ui.shadcn.com/
