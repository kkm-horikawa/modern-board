# FE-002-1: Layoutコンポーネントの実装

## 概要
アプリケーションの基本レイアウトを構成するコンポーネントを実装する。

**親タスク**: FE-002

## 優先度
**High**

## 難易度
**Easy**

## 前提条件
- [x] FE-001: プロジェクトセットアップが完了している
- [ ] UIフレームワーク/スタイリングシステムが選定されている

## 実装内容

### コンポーネント一覧（5-7個、PR1本で完結）

1. **Header** (`src/components/layout/Header.tsx`)
   - アプリケーションロゴ/タイトル
   - ナビゲーションリンク
   - モバイルメニューボタン（レスポンシブ対応）

2. **Footer** (`src/components/layout/Footer.tsx`)
   - コピーライト表示
   - フッターリンク（利用規約、プライバシーポリシー等）

3. **Sidebar** (`src/components/layout/Sidebar.tsx`)
   - カテゴリ一覧へのリンク
   - ドロワー/固定表示の切り替え（レスポンシブ）

4. **Container** (`src/components/layout/Container.tsx`)
   - コンテンツ幅の制限
   - パディング/マージンの統一

5. **MainLayout** (`src/components/layout/MainLayout.tsx`)
   - Header + Sidebar + Content + Footer の組み合わせ
   - レイアウトの基本構造

6. **MobileMenu** (`src/components/layout/MobileMenu.tsx`、オプション)
   - モバイル用ハンバーガーメニュー

## 受け入れ基準
- [ ] すべてのLayoutコンポーネントが実装されている
- [ ] TypeScript型定義が完備されている
- [ ] レスポンシブ対応されている（モバイル/タブレット/デスクトップ）
- [ ] Storybookストーリーが作成されている（オプション）
- [ ] 基本的なユニットテストが実装されている

## ファイル構成
```
src/components/layout/
├── Header.tsx
├── Header.test.tsx
├── Footer.tsx
├── Footer.test.tsx
├── Sidebar.tsx
├── Sidebar.test.tsx
├── Container.tsx
├── Container.test.tsx
├── MainLayout.tsx
├── MainLayout.test.tsx
└── index.ts  # エクスポート
```

## 関連タスク
- FE-002: 共通コンポーネントライブラリ（親タスク）
- FE-002-2: 基本UIコンポーネント（次のタスク）
- FE-003: スレッド一覧ページ（このLayoutを使用）

## 参考
- Layout Patterns: https://www.patterns.dev/react/layout-components
