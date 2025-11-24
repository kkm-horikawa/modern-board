# FE-002-2: 基本UIコンポーネントの実装

## 概要
再利用可能な基本UIコンポーネントを実装する。shadcn/ui等を使用する場合は、それをラップしたカスタムコンポーネントとして実装。

**親タスク**: FE-002

## 優先度
**High**

## 難易度
**Medium**

## 前提条件
- [x] FE-001: プロジェクトセットアップが完了している
- [x] FE-002-1: Layoutコンポーネントが完成している

## 実装内容

### フェーズ1: コア要素（PR 1本目、10-12個）

1. **Button** - ボタン（Primary, Secondary, Danger等）
2. **Input** - テキスト入力
3. **Textarea** - 複数行テキスト入力
4. **Select** - セレクトボックス
5. **Label** - ラベル
6. **ErrorMessage** - エラーメッセージ表示
7. **Spinner** - ローディングインジケーター
8. **Card** - カード
9. **Badge** - バッジ（NEW、HOT等）
10. **Divider** - 区切り線

### フェーズ2: インタラクティブ要素（PR 2本目、4-5個、オプション）

11. **Modal** - モーダルダイアログ
12. **Tooltip** - ツールチップ
13. **Checkbox** - チェックボックス
14. **Radio** - ラジオボタン

## 受け入れ基準
- [ ] すべての基本UIコンポーネントが実装されている
- [ ] TypeScript型定義が完備されている
- [ ] アクセシビリティ対応（ARIA属性、キーボードナビゲーション）
- [ ] バリアント/サイズのPropsが用意されている
- [ ] ユニットテストが実装されている
- [ ] ホバー/フォーカス/アクティブ状態が実装されている

## 実装例: Buttonコンポーネント

```typescript
// src/components/common/Button.tsx
import { ButtonHTMLAttributes, ReactNode } from 'react';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  className,
  ...props
}: ButtonProps) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size} ${className || ''}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? <Spinner size="sm" /> : children}
    </button>
  );
};
```

## ファイル構成
```
src/components/common/
├── Button.tsx
├── Button.test.tsx
├── Input.tsx
├── Input.test.tsx
├── Textarea.tsx
├── Textarea.test.tsx
├── Select.tsx
├── Select.test.tsx
├── Modal.tsx
├── Modal.test.tsx
├── Spinner.tsx
├── Spinner.test.tsx
├── Badge.tsx
├── Badge.test.tsx
├── Card.tsx
├── Card.test.tsx
└── index.ts
```

## 関連タスク
- FE-002: 共通コンポーネントライブラリ（親タスク）
- FE-002-1: Layoutコンポーネント（前提タスク）
- FE-002-3: 掲示板特化コンポーネント（次のタスク）
- FE-002-4: フォームコンポーネント（これらを使用）

## 参考
- Component API Design: https://www.smashingmagazine.com/2021/05/design-system-components-api/
- Accessible Components: https://www.a11y-101.com/development/components
