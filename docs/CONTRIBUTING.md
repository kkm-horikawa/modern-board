# コントリビューションガイド

Modern Boardプロジェクトへの貢献に興味を持っていただき、ありがとうございます！このドキュメントでは、プロジェクトへの貢献方法について説明します。

## 目次

- [行動規範](#行動規範)
- [開発環境のセットアップ](#開発環境のセットアップ)
- [ブランチ戦略](#ブランチ戦略)
- [コミットメッセージ規約](#コミットメッセージ規約)
- [プルリクエストの作成](#プルリクエストの作成)
- [コードレビュープロセス](#コードレビュープロセス)
- [コーディング規約](#コーディング規約)
- [テストの書き方](#テストの書き方)
- [Issue の作成](#issueの作成)

## 行動規範

プロジェクトに参加するすべての人に、敬意を持って接することを期待しています：

- 建設的なフィードバックを提供する
- 他の視点やアイデアを尊重する
- 初心者に対して親切で支援的である
- 個人攻撃や不適切なコメントを避ける

## 開発環境のセットアップ

貢献を始める前に、開発環境をセットアップしてください。詳細な手順は [DEVELOPMENT.md](./DEVELOPMENT.md) を参照してください。

### クイックスタート

1. リポジトリをフォーク
2. フォークしたリポジトリをクローン
   ```bash
   git clone https://github.com/YOUR_USERNAME/modern-board.git
   cd modern-board
   ```
3. 依存関係をインストール
   ```bash
   # バックエンド
   cd backend
   uv sync --extra dev

   # フロントエンド
   cd ../frontend
   npm install
   ```
4. 開発サーバーを起動して動作確認

## ブランチ戦略

プロジェクトでは Git Flow に基づいたブランチ戦略を採用しています。

### メインブランチ

- **`main`** (または `master`): 本番環境にデプロイされる安定版
- **`develop`**: 次のリリースに向けた開発ブランチ（存在する場合）

### 作業ブランチ

新しい機能や修正を行う際は、以下の命名規則に従ってブランチを作成してください：

```
feature/機能名    # 新機能の追加
bugfix/修正内容   # バグ修正
hotfix/修正内容   # 緊急の本番修正
docs/内容         # ドキュメントの更新
refactor/内容     # リファクタリング
test/内容         # テストの追加・修正
```

### ブランチ作成例

```bash
# 最新の main ブランチから作業ブランチを作成
git checkout main
git pull origin main
git checkout -b feature/add-user-profile

# 作業を行う
git add .
git commit -m "feat: ユーザープロフィール機能を追加"

# リモートにプッシュ
git push origin feature/add-user-profile
```

## コミットメッセージ規約

[Conventional Commits](https://www.conventionalcommits.org/) に従ったコミットメッセージを使用します。

### フォーマット

```
<type>: <subject>

<body>

<footer>
```

### Type（種類）

- **feat**: 新機能の追加
- **fix**: バグ修正
- **docs**: ドキュメントのみの変更
- **style**: コードの動作に影響しない変更（空白、フォーマット、セミコロンなど）
- **refactor**: バグ修正や機能追加を伴わないコードの変更
- **perf**: パフォーマンス改善
- **test**: テストの追加や修正
- **chore**: ビルドプロセスやツールの変更
- **ci**: CI/CD設定の変更

### 例

```bash
# 良い例
git commit -m "feat: スレッド検索機能を追加"
git commit -m "fix: 返信投稿時の文字数制限エラーを修正"
git commit -m "docs: READMEにセットアップ手順を追加"

# 詳細な説明を含む例
git commit -m "feat: ユーザー認証機能を実装

- JWT認証を使用
- ログイン/ログアウトエンドポイントを追加
- トークンリフレッシュ機能を実装

Closes #123"
```

### 日本語 vs 英語

コミットメッセージは日本語でも英語でも構いませんが、プロジェクト内で一貫性を保つようにしてください。

## プルリクエストの作成

### プルリクエスト作成前のチェックリスト

- [ ] コードが正常に動作する
- [ ] テストがすべて通過する
- [ ] Lintエラーがない
- [ ] ドキュメントが更新されている（必要な場合）
- [ ] コミットメッセージが規約に従っている

### テストとLintの実行

```bash
# バックエンド
cd backend
uv run pytest
uv run ruff check .
uv run ruff format .
uv run pyright

# フロントエンド
cd frontend
npm test
npm run lint
npm run format
```

### プルリクエストの作成手順

1. 作業ブランチをリモートにプッシュ
   ```bash
   git push origin feature/your-feature-name
   ```

2. GitHub でプルリクエストを作成
   - ベースブランチ: `main`（または `develop`）
   - 比較ブランチ: `feature/your-feature-name`

3. プルリクエストのテンプレートに従って記入
   - 変更内容の説明
   - 関連する Issue 番号
   - スクリーンショット（UI変更の場合）
   - テスト方法

### プルリクエストのテンプレート

```markdown
## 概要
この変更の目的と概要を説明してください。

## 変更内容
- 変更点1
- 変更点2
- 変更点3

## 関連Issue
Closes #issue_number

## テスト方法
1. ステップ1
2. ステップ2
3. 期待される結果

## スクリーンショット
（UI変更の場合は追加）

## チェックリスト
- [ ] テストが通過する
- [ ] Lintエラーがない
- [ ] ドキュメントを更新した
- [ ] 変更内容をローカルで確認した
```

## コードレビュープロセス

### レビューを受ける側

1. プルリクエストを作成したら、適切なレビュアーをアサイン
2. レビューコメントに対して真摯に対応
3. 修正が必要な場合は、同じブランチに追加のコミットをプッシュ
4. すべてのコメントに返信またはResolve
5. 承認後にマージ（またはメンテナーがマージ）

### レビューをする側

- 建設的で具体的なフィードバックを提供
- コードの動作を理解してから承認
- 小さな問題は Suggestion 機能を使用
- 重大な問題がある場合は Changes Requested でブロック
- 良いコードには積極的に Approve

### レビューで確認すべき項目

- [ ] コードが要件を満たしている
- [ ] バグや潜在的な問題がない
- [ ] テストが適切にカバーされている
- [ ] コーディング規約に従っている
- [ ] パフォーマンスへの影響を考慮している
- [ ] セキュリティの問題がない
- [ ] 命名が適切で理解しやすい
- [ ] ドキュメントが適切に更新されている

## コーディング規約

### Python（バックエンド）

[PEP 8](https://pep8-ja.readthedocs.io/ja/latest/) に基づき、Ruffでフォーマットを統一しています。

```python
# 良い例
def create_thread(title: str, content: str) -> Thread:
    """新しいスレッドを作成する

    Args:
        title: スレッドのタイトル
        content: 最初の投稿内容

    Returns:
        作成されたThreadオブジェクト
    """
    thread = Thread.objects.create(
        title=title,
        content=content,
    )
    return thread

# 悪い例
def createThread(title,content):  # 型アノテーションなし、キャメルケース
    thread=Thread.objects.create(title=title,content=content)  # スペースなし
    return thread
```

主要なルール:
- 行の長さ: 最大88文字
- インデント: スペース4つ
- 文字列: ダブルクォート `"`
- 型アノテーション必須
- 関数名: スネークケース `function_name`
- クラス名: パスカルケース `ClassName`
- 定数: 大文字スネークケース `CONSTANT_NAME`

### TypeScript/React（フロントエンド）

Biomeでフォーマットを統一しています。

```typescript
// 良い例
interface ThreadProps {
  id: number;
  title: string;
  createdAt: Date;
}

export const ThreadCard: React.FC<ThreadProps> = ({ id, title, createdAt }) => {
  const handleClick = () => {
    console.log(`Thread ${id} clicked`);
  };

  return (
    <div className="thread-card" onClick={handleClick}>
      <h2>{title}</h2>
      <time>{createdAt.toLocaleDateString()}</time>
    </div>
  );
};

// 悪い例
const ThreadCard = (props) => {  // 型定義なし
  return <div className='thread-card'>  // シングルクォート
    <h2>{props.title}</h2></div>  // 閉じタグが同じ行
}
```

主要なルール:
- 行の長さ: 最大100文字
- インデント: スペース2つ
- 文字列: ダブルクォート `"`
- セミコロン必須
- 関数名: キャメルケース `functionName`
- コンポーネント名: パスカルケース `ComponentName`
- 型定義を必ず使用

## テストの書き方

### バックエンドテスト（pytest）

```python
# api/tests/unit/test_models.py
import pytest
from api.models import Board, Thread

@pytest.mark.django_db
class TestThreadModel:
    """Threadモデルのテスト"""

    def test_thread_creation(self):
        """スレッドが正常に作成できること"""
        board = Board.objects.create(name="テスト板", slug="test")
        thread = Thread.objects.create(
            board=board,
            title="テストスレッド",
            content="テスト内容"
        )

        assert thread.title == "テストスレッド"
        assert thread.board == board
        assert thread.post_count == 0

    def test_thread_str_representation(self):
        """スレッドの文字列表現が正しいこと"""
        board = Board.objects.create(name="テスト板", slug="test")
        thread = Thread.objects.create(
            board=board,
            title="テストスレッド",
            content="テスト内容"
        )

        assert str(thread) == "テストスレッド"
```

### フロントエンドテスト（Vitest + React Testing Library）

```typescript
// src/components/ThreadCard.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ThreadCard } from "./ThreadCard";

describe("ThreadCard", () => {
  it("スレッド情報が正しく表示される", () => {
    const thread = {
      id: 1,
      title: "テストスレッド",
      createdAt: new Date("2024-01-01"),
    };

    render(<ThreadCard {...thread} />);

    expect(screen.getByText("テストスレッド")).toBeInTheDocument();
    expect(screen.getByText("2024/1/1")).toBeInTheDocument();
  });

  it("クリック時にコールバックが呼ばれる", () => {
    const handleClick = vi.fn();
    const thread = {
      id: 1,
      title: "テストスレッド",
      createdAt: new Date("2024-01-01"),
    };

    render(<ThreadCard {...thread} onClick={handleClick} />);

    fireEvent.click(screen.getByRole("article"));

    expect(handleClick).toHaveBeenCalledWith(1);
  });
});
```

### テストのガイドライン

- **ユニットテスト**: 個々の関数やメソッドをテスト
- **統合テスト**: 複数のコンポーネントの連携をテスト
- **E2Eテスト**: ユーザーの操作フローをテスト

テストは以下を満たすように書く:
- 1つのテストで1つのことをテストする
- テスト名は「何をテストするか」を明確に表す
- テストは独立して実行可能
- テストは決定論的（毎回同じ結果）

## Issue の作成

バグ報告や機能リクエストは、GitHub Issues で管理しています。

### バグ報告

以下の情報を含めてください:

```markdown
## 問題の説明
何が問題なのか簡潔に説明してください。

## 再現手順
1. ステップ1
2. ステップ2
3. エラーが発生する

## 期待される動作
本来どうあるべきか説明してください。

## 実際の動作
実際に何が起こったか説明してください。

## 環境
- OS: macOS 14.0
- ブラウザ: Chrome 120
- Python: 3.13
- Node.js: 20.0

## スクリーンショット/ログ
該当する場合は追加してください。
```

### 機能リクエスト

```markdown
## 機能の説明
実装したい機能を説明してください。

## 動機
なぜこの機能が必要なのか説明してください。

## 提案する実装
どのように実装すべきか（任意）

## 代替案
検討した他のアプローチ（任意）
```

## よくある質問

### Q: どこから始めればいいですか？

A: まずは "good first issue" ラベルの付いた Issue から始めることをお勧めします。開発環境のセットアップ方法は [DEVELOPMENT.md](./DEVELOPMENT.md) を参照してください。

### Q: コードレビューにはどれくらい時間がかかりますか？

A: 通常、数日以内にレビューが行われます。ただし、規模や内容によって変わる場合があります。

### Q: プルリクエストがマージされない場合は？

A: レビューコメントに対応し、必要な修正を行ってください。質問がある場合は、遠慮なくコメントで質問してください。

### Q: ドキュメントの誤字を見つけました。

A: 小さな修正でもプルリクエストは大歓迎です！ドキュメントの改善はプロジェクトにとって非常に重要です。

## 謝辞

プロジェクトへの貢献に感謝します！あなたの貢献が Modern Board をより良いものにします。

## 連絡先

質問や提案がある場合は、以下の方法でお問い合わせください:

- GitHub Issues: バグ報告や機能リクエスト
- GitHub Discussions: 一般的な質問や議論

---

このガイドラインは随時更新される可能性があります。最新版は常にリポジトリで確認してください。
