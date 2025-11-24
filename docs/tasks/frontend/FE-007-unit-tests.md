# FE-007: フロントエンドユニットテストの実装

## 概要
Vitestを使用してフロントエンドのユニットテストを実装し、コンポーネントやロジックの品質を保証する。

## 優先度
**Medium** - リリース前に必要

## 難易度
**Medium**

## 前提条件
- [x] FE-001: プロジェクトセットアップが完了
- [x] FE-002: 共通コンポーネントが実装済み
- [x] FE-003-005: 主要ページが実装済み

## 実装内容

### 1. テスト環境のセットアップ
- [ ] Vitestのインストールと設定
- [ ] @testing-library/reactのインストール
- [ ] @testing-library/user-eventのインストール
- [ ] jest-domのセットアップ
- [ ] MSW（Mock Service Worker）のセットアップ（API モック用）
- [ ] カバレッジ設定

**vitest.config.ts例:**
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/tests/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/tests/',
      ],
    },
  },
});
```

### 2. 共通コンポーネントのテスト

#### 2.1 基本UIコンポーネント
- [ ] `Button` コンポーネント
  - クリックイベントのテスト
  - disabled状態のテスト
  - variant（Primary, Secondary等）のテスト
- [ ] `Input` コンポーネント
  - 入力値の変更テスト
  - バリデーションエラー表示のテスト
  - disabled状態のテスト
- [ ] `Modal` コンポーネント
  - 開閉のテスト
  - Escキーで閉じるテスト
  - 背景クリックで閉じるテスト
- [ ] その他基本コンポーネント

#### 2.2 掲示板特化コンポーネント
- [ ] `ThreadCard` コンポーネント
  - レンダリングのテスト
  - クリックでナビゲートするテスト
  - バッジ表示のテスト
- [ ] `PostItem` コンポーネント
  - 投稿内容の表示テスト
  - リアクションボタンのテスト
- [ ] `ReactionButton` コンポーネント
  - クリックでリアクション追加のテスト
  - 数のカウント表示テスト

### 3. ページコンポーネントのテスト

#### 3.1 スレッド一覧ページ
- [ ] スレッド一覧の表示テスト
- [ ] ローディング状態のテスト
- [ ] エラー状態のテスト
- [ ] フィルタ機能のテスト
- [ ] ソート機能のテスト
- [ ] ページネーションのテスト

#### 3.2 スレッド詳細ページ
- [ ] スレッド詳細の表示テスト
- [ ] 投稿一覧の表示テスト
- [ ] 投稿作成フォームのテスト
- [ ] リアクション追加のテスト
- [ ] アンカーリンクのテスト

#### 3.3 スレッド作成ページ
- [ ] フォーム表示のテスト
- [ ] バリデーションのテスト
- [ ] 送信処理のテスト
- [ ] エラーハンドリングのテスト

### 4. カスタムフックのテスト
- [ ] データフェッチ用フックのテスト
- [ ] フォーム管理用フックのテスト
- [ ] 状態管理用フックのテスト

### 5. ユーティリティ関数のテスト
- [ ] 日時フォーマット関数
- [ ] バリデーション関数
- [ ] 文字列処理関数
- [ ] API クライアント関数

### 6. API モック（MSW）
- [ ] ハンドラーの定義
  ```typescript
  import { http, HttpResponse } from 'msw';

  export const handlers = [
    http.get('/api/v1/threads/', () => {
      return HttpResponse.json({
        count: 10,
        results: [/* ... */],
      });
    }),
  ];
  ```
- [ ] テストごとのモック上書き
- [ ] エラーレスポンスのモック

### 7. アクセシビリティテスト
- [ ] jest-axe の導入
- [ ] 主要コンポーネントのa11yテスト
- [ ] ARIA属性の検証

### 8. スナップショットテスト
- [ ] 重要なコンポーネントのスナップショット作成
- [ ] 変更検知の仕組み確立

### 9. CI統合
- [ ] GitHub Actionsでのテスト実行
- [ ] カバレッジレポートの生成
- [ ] PRへのカバレッジコメント

## 受け入れ基準
- [ ] 共通コンポーネントのテストカバレッジ80%以上
- [ ] ページコンポーネントのテストカバレッジ70%以上
- [ ] ユーティリティ関数のテストカバレッジ90%以上
- [ ] すべてのテストがパスする
- [ ] CIでテストが自動実行される
- [ ] テスト実行時間が妥当（5分以内）
- [ ] アクセシビリティテストがパスする

## テスト例

### Button コンポーネント
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    await userEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

### ThreadCard コンポーネント
```typescript
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect } from 'vitest';
import { ThreadCard } from './ThreadCard';

describe('ThreadCard', () => {
  const mockThread = {
    id: 1,
    title: 'Test Thread',
    category: { id: 1, name: 'General' },
    post_count: 42,
    view_count: 100,
    is_pinned: false,
  };

  it('renders thread information', () => {
    render(
      <BrowserRouter>
        <ThreadCard thread={mockThread} />
      </BrowserRouter>
    );

    expect(screen.getByText('Test Thread')).toBeInTheDocument();
    expect(screen.getByText('General')).toBeInTheDocument();
    expect(screen.getByText('42')).toBeInTheDocument();
  });

  it('shows pinned indicator when thread is pinned', () => {
    render(
      <BrowserRouter>
        <ThreadCard thread={{ ...mockThread, is_pinned: true }} />
      </BrowserRouter>
    );

    expect(screen.getByLabelText(/pinned/i)).toBeInTheDocument();
  });
});
```

## カバレッジ目標
- **全体**: 75%以上
- **共通コンポーネント**: 80%以上
- **ビジネスロジック**: 90%以上
- **ユーティリティ**: 90%以上

## 関連タスク
- FE-002: コンポーネントライブラリ
- FE-003: スレッド一覧ページ
- FE-004: スレッド詳細ページ
- FE-005: スレッド作成ページ
- INT-001: E2Eテスト

## 参考
- Vitest: https://vitest.dev/
- Testing Library: https://testing-library.com/react
- MSW: https://mswjs.io/
- jest-axe: https://github.com/nickcolley/jest-axe
- Testing Best Practices: https://kentcdodds.com/blog/common-mistakes-with-react-testing-library
