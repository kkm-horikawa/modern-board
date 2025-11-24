## 📝 新規Issue作成タスク

**目的：マージ済みPRを分析して、新しいIssueを作成する**

---

## 📋 実行手順

### 1. マージ済みPRを分析

```bash
# 過去7日間のマージ済みPRを確認
gh pr list --state merged --limit 10 --json number,title,mergedAt,files

# 各PRの詳細を確認
gh pr view {PR_NUMBER} --json files,additions,deletions,body
```

### 2. 改善点を見つける

各マージ済みPRについて以下をチェック：

**バグの可能性：**
- エラーハンドリングは十分か？
- エッジケースは考慮されているか？
- 型安全性は保たれているか？

**パフォーマンス：**
- 無駄な処理はないか？
- データベースクエリは最適化されているか？
- メモリリークの可能性はないか？

**セキュリティ：**
- 入力バリデーションは十分か？
- 認証・認可は適切か？
- 機密情報の漏洩リスクはないか？

**テスト：**
- テストカバレッジは十分か？
- 重要なケースがテストされているか？
- 統合テストは必要か？

**ドキュメント：**
- APIドキュメントは更新されているか？
- README は最新か？
- 使用例は記載されているか？

### 3. 新しいIssueを作成

見つけた改善点について、Issueを作成してください：

#### Bug Issue

```bash
gh issue create \
  --title "Bug: {問題の要約}" \
  --body "## 概要

PR #{PR_NUMBER} でマージされた実装に以下の問題があります。

## 問題の詳細

{具体的な問題}

## 再現手順

1. ステップ1
2. ステップ2

## 期待される動作

{期待される動作}

## 提案される修正

{修正案}

## 関連PR

- #{PR_NUMBER}" \
  --label "bug,priority:high"
```

#### Enhancement Issue

```bash
gh issue create \
  --title "Enhancement: {改善内容}" \
  --body "## 概要

PR #{PR_NUMBER} の実装に対する改善提案です。

## 現状

{現在の実装}

## 提案

{改善提案}

## 期待される効果

- 効果1
- 効果2

## 関連PR

- #{PR_NUMBER}" \
  --label "enhancement,priority:medium"
```

#### Test Issue

```bash
gh issue create \
  --title "Test: {テスト追加}" \
  --body "## 概要

PR #{PR_NUMBER} の実装に対するテスト追加提案です。

## 不足しているテスト

- テストケース1
- テストケース2

## テスト内容

{具体的なテスト内容}

## 関連PR

- #{PR_NUMBER}" \
  --label "testing,priority:medium"
```

### 4. 次のマイルストーンのタスクを提案

```bash
# マイルストーンの進捗を確認
gh api repos/:owner/:repo/milestones --jq '.[] | select(.state=="open") | {number, title, open_issues, closed_issues}'

# 完了が近いマイルストーンに対して、次のタスクを提案
gh issue create \
  --title "Feature: {次の機能}" \
  --body "## 概要

マイルストーン「{マイルストーン名}」の次の機能として提案します。

## 機能詳細

{詳細}

## 実装方針

{方針}" \
  --label "enhancement,priority:medium" \
  --milestone "{MILESTONE_NUMBER}"
```

---

## 📝 完了報告

以下の形式で報告してください：

### 作成したIssue

1. **Issue #{番号}: {タイトル}** ({Bug/Enhancement/Test})
   - 対象PR: #{PR番号}
   - 理由: {なぜ作成したか}
   - 優先度: {priority}

2. **Issue #{番号}: {タイトル}**
   - ...

### 分析したPR

- PR #{番号}: {タイトル} - {分析結果}

---

## 🎯 完了基準

- [ ] 最近のマージ済みPRを少なくとも3つ分析
- [ ] 少なくとも **2つの新しいIssue** を作成
- [ ] 作成したIssueを報告

**完了したら、このIssueをクローズしてください。**

---

## ⚠️ 重要

- **具体的な改善点を見つけてください**（抽象的な提案ではなく）
- **実装可能なIssueを作成してください**
- **適切なラベルと優先度を設定してください**
- **次のタスクが途切れないようにしてください**
