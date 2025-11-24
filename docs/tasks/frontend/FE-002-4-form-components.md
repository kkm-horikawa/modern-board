# FE-002-4: フォームコンポーネントの実装

## 概要
フォーム入力を簡単にするためのラッパーコンポーネントを実装し、React Hook Formとの統合を容易にする。

**親タスク**: FE-002

## 優先度
**High**

## 難易度
**Easy**

## 前提条件
- [x] FE-002-2: 基本UIコンポーネントが完成している
- [ ] React Hook FormとZodがインストールされている

## 実装内容

### コンポーネント一覧（3-5個、PR 1本で完結）

1. **FormField** (`src/components/forms/FormField.tsx`)
   - ラベル + 入力フィールド + エラーメッセージ のラッパー
   - React Hook Formと統合

2. **FormGroup** (`src/components/forms/FormGroup.tsx`)
   - 複数のFormFieldをグループ化

3. **FormLabel** (`src/components/forms/FormLabel.tsx`)
   - フォームラベル（必須マーク対応）

4. **FormError** (`src/components/forms/FormError.tsx`)
   - フォームエラー表示

5. **FormHelperText** (`src/components/forms/FormHelperText.tsx`)
   - ヘルパーテキスト表示

## 受け入れ基準
- [ ] すべてのフォームコンポーネントが実装されている
- [ ] React Hook Formと統合されている
- [ ] TypeScript型定義が完備されている
- [ ] エラー状態が適切に表示される
- [ ] アクセシビリティ対応（適切なaria-*属性）
- [ ] ユニットテストが実装されている

## 実装例: FormFieldコンポーネント

```typescript
// src/components/forms/FormField.tsx
import { ReactNode } from 'react';
import { UseFormRegisterReturn } from 'react-hook-form';
import { Input } from '@/components/common/Input';
import { FormLabel } from './FormLabel';
import { FormError } from './FormError';
import { FormHelperText } from './FormHelperText';

export interface FormFieldProps {
  label: string;
  name: string;
  type?: string;
  required?: boolean;
  error?: string;
  helperText?: string;
  registration: UseFormRegisterReturn;
  children?: ReactNode;
}

export const FormField = ({
  label,
  name,
  type = 'text',
  required = false,
  error,
  helperText,
  registration,
  children,
}: FormFieldProps) => {
  return (
    <div className="form-field">
      <FormLabel htmlFor={name} required={required}>
        {label}
      </FormLabel>

      {children || (
        <Input
          id={name}
          type={type}
          aria-invalid={!!error}
          aria-describedby={error ? `${name}-error` : undefined}
          {...registration}
        />
      )}

      {error && <FormError id={`${name}-error`}>{error}</FormError>}
      {helperText && !error && (
        <FormHelperText>{helperText}</FormHelperText>
      )}
    </div>
  );
};
```

## 使用例

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { FormField } from '@/components/forms/FormField';

const schema = z.object({
  title: z.string().min(1, 'タイトルを入力してください'),
  content: z.string().min(1, '内容を入力してください'),
});

type FormData = z.infer<typeof schema>;

export const MyForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = (data: FormData) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <FormField
        label="タイトル"
        name="title"
        required
        error={errors.title?.message}
        registration={register('title')}
      />

      <FormField
        label="内容"
        name="content"
        required
        error={errors.content?.message}
        registration={register('content')}
      >
        <Textarea {...register('content')} />
      </FormField>

      <Button type="submit">送信</Button>
    </form>
  );
};
```

## ファイル構成
```
src/components/forms/
├── FormField.tsx
├── FormField.test.tsx
├── FormGroup.tsx
├── FormGroup.test.tsx
├── FormLabel.tsx
├── FormLabel.test.tsx
├── FormError.tsx
├── FormError.test.tsx
├── FormHelperText.tsx
├── FormHelperText.test.tsx
└── index.ts
```

## 関連タスク
- FE-002: 共通コンポーネントライブラリ（親タスク）
- FE-002-2: 基本UIコンポーネント（前提タスク）
- FE-005: スレッド作成ページ（これらを使用）

## 参考
- React Hook Form: https://react-hook-form.com/
- Form Patterns: https://www.patterns.dev/react/forms
- Accessible Forms: https://www.w3.org/WAI/tutorials/forms/
