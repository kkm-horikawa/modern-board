# FE-002-3: 掲示板特化コンポーネントの実装

## 概要
掲示板アプリケーション特有のビジネスロジックを持つコンポーネントを実装する。

**親タスク**: FE-002

## 優先度
**High**

## 難易度
**Medium**

## 前提条件
- [x] FE-002-1: Layoutコンポーネントが完成している
- [x] FE-002-2: 基本UIコンポーネントが完成している

## 実装内容

### コンポーネント一覧（8-11個、PR 1-2本で完結）

1. **ThreadCard** (`src/components/features/ThreadCard.tsx`)
   - スレッド一覧表示用カード
   - タイトル、カテゴリ、タグ、投稿数、閲覧数表示
   - ピン留め/トレンド/ロック表示

2. **PostItem** (`src/components/features/PostItem.tsx`)
   - 投稿アイテム
   - 投稿番号、投稿者名、日時、内容表示
   - リアクションボタン、返信リンク

3. **ReactionButton** (`src/components/features/ReactionButton.tsx`)
   - リアクションボタン（いいね、笑、驚き等）
   - クリックでリアクション追加
   - リアクション数表示

4. **CategoryBadge** (`src/components/features/CategoryBadge.tsx`)
   - カテゴリバッジ
   - カラーコーディング

5. **TagChip** (`src/components/features/TagChip.tsx`)
   - タグチップ
   - クリックでタグフィルタ

6. **TrendingIndicator** (`src/components/features/TrendingIndicator.tsx`)
   - トレンド表示（炎アイコン等）

7. **PinnedIndicator** (`src/components/features/PinnedIndicator.tsx`)
   - ピン留め表示（ピンアイコン）

8. **LockedIndicator** (`src/components/features/LockedIndicator.tsx`)
   - ロック表示（鍵アイコン）

9. **Pagination** (`src/components/features/Pagination.tsx`)
   - ページネーション
   - 前/次ボタン、ページ番号表示

10. **SortSelector** (`src/components/features/SortSelector.tsx`)
    - ソート選択UI
    - 最新順、投稿数順、閲覧数順等

11. **FilterPanel** (`src/components/features/FilterPanel.tsx`、オプション)
    - フィルタパネル
    - カテゴリ、タグ、ステータスフィルタ

## 受け入れ基準
- [ ] すべての掲示板特化コンポーネントが実装されている
- [ ] TypeScript型定義が完備されている（API型と連携）
- [ ] クリック等のイベントハンドラーが適切に実装されている
- [ ] レスポンシブ対応されている
- [ ] ユニットテストが実装されている
- [ ] アクセシビリティ対応されている

## 実装例: ThreadCardコンポーネント

```typescript
// src/components/features/ThreadCard.tsx
import { Thread } from '@/types/api';
import { Card } from '@/components/common/Card';
import { CategoryBadge } from './CategoryBadge';
import { TagChip } from './TagChip';
import { PinnedIndicator } from './PinnedIndicator';
import { TrendingIndicator } from './TrendingIndicator';

export interface ThreadCardProps {
  thread: Thread;
  onClick?: () => void;
}

export const ThreadCard = ({ thread, onClick }: ThreadCardProps) => {
  return (
    <Card onClick={onClick} className="cursor-pointer hover:shadow-lg">
      <div className="flex items-center gap-2 mb-2">
        {thread.is_pinned && <PinnedIndicator />}
        {thread.is_trending && <TrendingIndicator />}
        <CategoryBadge category={thread.category} />
      </div>

      <h3 className="text-lg font-bold mb-2">{thread.title}</h3>

      <div className="flex flex-wrap gap-1 mb-2">
        {thread.tags.slice(0, 5).map((tag) => (
          <TagChip key={tag.id} tag={tag} />
        ))}
      </div>

      <div className="flex gap-4 text-sm text-gray-600">
        <span>{thread.post_count} 投稿</span>
        <span>{thread.view_count} 閲覧</span>
        <span>{formatDate(thread.last_post_at)}</span>
      </div>
    </Card>
  );
};
```

## ファイル構成
```
src/components/features/
├── ThreadCard.tsx
├── ThreadCard.test.tsx
├── PostItem.tsx
├── PostItem.test.tsx
├── ReactionButton.tsx
├── ReactionButton.test.tsx
├── CategoryBadge.tsx
├── CategoryBadge.test.tsx
├── TagChip.tsx
├── TagChip.test.tsx
├── TrendingIndicator.tsx
├── PinnedIndicator.tsx
├── LockedIndicator.tsx
├── Pagination.tsx
├── Pagination.test.tsx
├── SortSelector.tsx
├── SortSelector.test.tsx
└── index.ts
```

## 関連タスク
- FE-002: 共通コンポーネントライブラリ（親タスク）
- FE-002-2: 基本UIコンポーネント（前提タスク）
- FE-003: スレッド一覧ページ（これらを使用）
- FE-004: スレッド詳細ページ（これらを使用）

## 参考
- Compound Components Pattern: https://www.patterns.dev/react/compound-pattern
