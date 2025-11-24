# INT-001: E2Eテストの実装

## 概要
Playwrightを使用したエンドツーエンド（E2E）テストを実装し、ユーザーフローの動作を保証する。

## 優先度
**Medium** - リリース前に必要

## 難易度
**Medium**

## 前提条件
- [x] フロントエンドの主要ページが実装済み
- [x] バックエンドAPIが実装済み
- [ ] テスト環境が整っている

## 実装内容

### 1. Playwrightのセットアップ
- [ ] Playwrightのインストール
- [ ] ブラウザのインストール（Chromium, Firefox, WebKit）
- [ ] 設定ファイル（`playwright.config.ts`）の作成
- [ ] テストディレクトリ構造の確立

```
frontend/
├── e2e/
│   ├── fixtures/          # テストフィクスチャ
│   ├── pages/             # Page Object Model
│   ├── tests/             # テストケース
│   └── playwright.config.ts
```

### 2. Page Object Modelの実装
- [ ] ThreadListPage クラス
- [ ] ThreadDetailPage クラス
- [ ] ThreadCreatePage クラス
- [ ] 共通コンポーネント（Header, Sidebar等）

### 3. ユーザーフローテスト

#### 3.1 スレッド閲覧フロー
- [ ] トップページにアクセス
- [ ] スレッド一覧が表示される
- [ ] スレッドをクリックして詳細ページへ遷移
- [ ] 投稿一覧が表示される
- [ ] スクロールして追加投稿を読む

#### 3.2 スレッド作成フロー
- [ ] 「スレッドを作成」ボタンをクリック
- [ ] スレッド作成フォームが表示される
- [ ] タイトル、カテゴリ、初回投稿を入力
- [ ] タグを選択
- [ ] 作成ボタンをクリック
- [ ] 新しいスレッドの詳細ページに遷移
- [ ] 作成したスレッドが表示される

#### 3.3 投稿作成フロー
- [ ] スレッド詳細ページにアクセス
- [ ] 投稿フォームに内容を入力
- [ ] 投稿ボタンをクリック
- [ ] 新しい投稿が表示される
- [ ] 投稿番号が正しく採番される

#### 3.4 リアクションフロー
- [ ] 投稿のリアクションボタンをクリック
- [ ] リアクション数が増加する
- [ ] 同じリアクションを再度クリック
- [ ] 適切なエラーまたは制限が表示される

#### 3.5 フィルタ・ソートフロー
- [ ] カテゴリフィルタを選択
- [ ] 該当カテゴリのスレッドのみ表示される
- [ ] タグフィルタを選択
- [ ] 該当タグのスレッドのみ表示される
- [ ] ソート条件を変更
- [ ] スレッドの順序が変わる

### 4. エッジケーステスト
- [ ] 存在しないスレッドIDにアクセス（404エラー）
- [ ] バリデーションエラー（空のタイトル等）
- [ ] ネットワークエラーのハンドリング
- [ ] ロックされたスレッドへの投稿試行
- [ ] 大量データでのパフォーマンス

### 5. クロスブラウザテスト
- [ ] Chromium でのテスト
- [ ] Firefox でのテスト
- [ ] WebKit（Safari）でのテスト

### 6. レスポンシブテスト
- [ ] デスクトップビュー（1920x1080）
- [ ] タブレットビュー（768x1024）
- [ ] モバイルビュー（375x667）

### 7. アクセシビリティテスト
- [ ] キーボードナビゲーション
- [ ] スクリーンリーダー対応確認
- [ ] ARIA属性の検証
- [ ] コントラスト比の確認

### 8. パフォーマンステスト
- [ ] ページロード時間の計測
- [ ] LCP, FID, CLSの計測
- [ ] リソースサイズの確認

### 9. CI/CD統合
- [ ] GitHub Actionsでの自動実行
- [ ] テスト結果のレポート生成
- [ ] スクリーンショットの保存（失敗時）
- [ ] ビデオ録画（失敗時）

## 受け入れ基準
- [ ] 主要なユーザーフローがテストされている
- [ ] テストが安定して成功する（flaky testがない）
- [ ] クロスブラウザで動作する
- [ ] レスポンシブ対応が確認されている
- [ ] CI/CDで自動実行される
- [ ] テスト実行時間が妥当（10分以内目標）
- [ ] テスト結果が分かりやすくレポートされる

## playwright.config.ts 例
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e/tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

## 関連タスク
- FE-003: スレッド一覧ページ
- FE-004: スレッド詳細ページ
- FE-005: スレッド作成フォーム
- BE-001: API統合テスト

## 参考
- Playwright: https://playwright.dev/
- Page Object Model: https://playwright.dev/docs/pom
- Best Practices: https://playwright.dev/docs/best-practices
