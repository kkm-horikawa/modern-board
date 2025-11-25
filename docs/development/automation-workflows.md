# 自動化ワークフロー

## TL;DR
- **PRドキュメントチェック**: PR作成時に自動実行し、ドキュメント必要性を確認
- **ドキュメント整理**: 毎週月曜11:00 JST（2:00 UTC）に自動実行
- **Issue分解**: 毎日10:00/16:00 JST（1:00/7:00 UTC）に自動実行

## 概要

このプロジェクトでは、開発効率を向上させるために3つの自動化ワークフローを使用しています。これらのワークフローはすべてClaudeを活用し、プロジェクトのドキュメント管理とIssue管理を自動化します。

## ワークフロー詳細

### 1. ドキュメントチェッカー (`claude-doc-checker.yml`)

#### 目的
新しいPRが作成された際に、そのPRに適切なドキュメントが必要かどうかを自動的にチェックします。

#### トリガー
- PRが作成（opened）されたとき
- 手動実行（workflow_dispatch）

#### 動作フロー
1. PRが作成されると自動的に起動
2. ドキュメントチェックタスク用のIssueを作成
   - タイトル形式: `DOC-CHECK-{日時}: PR #{PR番号} のドキュメントチェック`
   - テンプレート: `.github/templates/doc-pr-check-task.md`
   - ラベル: `automation`, `documentation`
3. 作成したIssueに`@claude`メンションでClaudeを起動
4. ClaudeがPRの変更内容を分析し、ドキュメントの必要性を判断

#### 手動実行
```bash
gh workflow run claude-doc-checker.yml -f pr_number=<PR番号>
```

#### 必要な権限
- `contents: read` - リポジトリの読み取り
- `issues: write` - Issue作成・編集
- `pull-requests: write` - PR情報の読み取り・編集

### 2. ドキュメント整理 (`claude-doc-organizer.yml`)

#### 目的
プロジェクトのドキュメント構造を定期的に整理し、一貫性と可読性を維持します。

#### トリガー
- スケジュール: 毎週月曜 11:00 JST（2:00 UTC）
- 手動実行（workflow_dispatch）

#### 動作フロー
1. スケジュールまたは手動で起動
2. ドキュメント整理タスク用のIssueを作成
   - タイトル形式: `DOC-ORG-{日時}: ドキュメント整理タスク`
   - テンプレート: `.github/templates/doc-organization-task.md`
   - ラベル: `automation`, `documentation-org`
3. 作成したIssueに`@claude`メンションでClaudeを起動
4. Claudeがドキュメント全体を分析し、整理・改善を実施

#### 手動実行
```bash
gh workflow run claude-doc-organizer.yml
```

#### 必要な権限
- `contents: write` - ドキュメントファイルの編集
- `issues: write` - Issue作成・編集
- `pull-requests: write` - PR作成

### 3. Issue分解 (`claude-issue-decomposer.yml`)

#### 目的
大きなIssueを実装可能な小さなタスクに自動的に分解し、開発の進めやすさを向上させます。

#### トリガー
- スケジュール: 毎日 10:00, 16:00 JST（1:00, 7:00 UTC）
- 手動実行（workflow_dispatch）

#### 動作フロー
1. スケジュールまたは手動で起動
2. Issue分解タスク用のIssueを作成
   - タイトル形式: `DECOMP-{日時}: Issue分解タスク`
   - テンプレート: `.github/templates/issue-decomposition-task.md`
   - ラベル: `automation`, `decomposition`
3. 作成したIssueに`@claude`メンションでClaudeを起動
4. Claudeが大きなIssueを検索し、実装可能な小さなタスクに分解

#### 手動実行
```bash
gh workflow run claude-issue-decomposer.yml
```

#### 必要な権限
- `contents: read` - リポジトリの読み取り
- `issues: write` - Issue作成・編集

## 共通仕様

### 技術スタック
- **ランタイム**: Ubuntu Latest
- **パッケージマネージャー**: Bun (latest)
- **ブランチ**: develop
- **認証**: `PAT_TOKEN` シークレット使用

### テンプレートファイル
すべてのワークフローは、`.github/templates/`ディレクトリ内のMarkdownテンプレートを使用してIssueを作成します。

- `doc-pr-check-task.md` - ドキュメントチェック用
- `doc-organization-task.md` - ドキュメント整理用
- `issue-decomposition-task.md` - Issue分解用

### ラベリング
各ワークフローは特定のラベルを使用してIssueを分類します：

- `automation` - すべての自動化タスクに付与
- `documentation` - ドキュメントチェックタスク
- `documentation-org` - ドキュメント整理タスク
- `decomposition` - Issue分解タスク

## トラブルシューティング

### ワークフローが起動しない
- `PAT_TOKEN`シークレットが正しく設定されているか確認
- ワークフローファイルの権限設定を確認
- GitHub Actionsが有効になっているか確認

### Claudeが応答しない
- Issue内の`@claude`メンションが正しいか確認
- Claude Code Actionが正しく設定されているか確認
- Issueのラベルが正しく付与されているか確認

### スケジュールが実行されない
- リポジトリが公開されているか、GitHub Actionsの分数制限内か確認
- cronスケジュールが正しいタイムゾーン（UTC）で設定されているか確認
- デフォルトブランチ（develop）にワークフローファイルが存在するか確認

## 関連ドキュメント

- [CONTRIBUTING.md](../CONTRIBUTING.md) - コントリビューションガイドライン
- [DEVELOPMENT.md](../DEVELOPMENT.md) - 開発環境セットアップ
- [DESIGN.md](../DESIGN.md) - プロジェクト設計ドキュメント

## 参考リンク

- [GitHub Actions ドキュメント](https://docs.github.com/ja/actions)
- [Claude Code Action](https://github.com/anthropics/claude-code-action)
- [Cron式リファレンス](https://crontab.guru/)

---
最終更新: 2025-11-25
