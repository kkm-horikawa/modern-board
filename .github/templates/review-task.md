## 🔍 PRレビュー・マージタスク

**目的：Ready for ReviewのPRをレビューして、承認済みのPRをマージする**

---

## 📋 実行手順

### 1. Ready for ReviewのPRを確認

```bash
# Ready for ReviewのPRを確認
gh pr list --state open --json number,title,isDraft,reviews,reviewDecision

# Draft PRは除外
gh pr list --state open --json number,title,isDraft | jq '.[] | select(.isDraft == false)'
```

### 2. PRをレビュー

レビューすべきPRを1つ選択して、詳細にレビューしてください：

```bash
# PRの詳細を確認
gh pr view {PR_NUMBER}

# ブランチ名を取得
BRANCH_NAME=$(gh pr view {PR_NUMBER} --json headRefName --jq '.headRefName')
echo "ブランチ名: $BRANCH_NAME"

# 変更内容を確認
gh pr diff {PR_NUMBER}

# ファイル一覧を確認
gh pr view {PR_NUMBER} --json files | jq '.files[] | {path, additions, deletions}'
```

**レビュー観点：**

#### コード品質
- [ ] コードは読みやすいか？
- [ ] 適切な命名規則が使われているか？
- [ ] 不要なコードはないか？
- [ ] 適切にコメントされているか？

#### 機能
- [ ] 要件を満たしているか？
- [ ] エッジケースは考慮されているか？
- [ ] エラーハンドリングは適切か？

#### テスト
- [ ] テストコードは十分か？
- [ ] 重要なケースがカバーされているか？
- [ ] テストは pass しているか？

#### セキュリティ
- [ ] 入力バリデーションはあるか？
- [ ] SQLインジェクションの危険はないか？
- [ ] XSSの危険はないか？
- [ ] 認証・認可は適切か？

#### パフォーマンス
- [ ] パフォーマンス上の問題はないか？
- [ ] 無駄な処理はないか？
- [ ] データベースクエリは最適か？

#### ドキュメント
- [ ] ドキュメントは更新されているか？
- [ ] APIドキュメントは正しいか？

### 3. レビュー結果に基づいてアクションを実行

**重要：必ず以下のどちらかを実行してください**

#### A. 問題がない場合 → 承認してマージ

```bash
# 承認する
gh pr review {PR_NUMBER} --approve --body "LGTM! 問題ありません。マージします。

**確認した点：**
- コード品質 ✓
- テストカバレッジ ✓
- セキュリティ ✓
- パフォーマンス ✓
- ドキュメント ✓"

# すぐにマージ
gh pr merge {PR_NUMBER} --squash --delete-branch

# 関連Issueをクローズ
gh issue close {ISSUE_NUMBER} --comment "PR #{PR_NUMBER} でマージ完了しました。"
```

#### B. 問題がある場合 → Issueを発行

```bash
# レビューコメントを投稿
gh pr review {PR_NUMBER} --comment --body "レビューしました。いくつか問題があるため、修正用のIssueを作成します。"

# ブランチ名を取得
BRANCH_NAME=$(gh pr view {PR_NUMBER} --json headRefName --jq '.headRefName')

# 問題点をまとめたIssueを作成
gh issue create \
  --title "Fix: PR #{PR_NUMBER} (${BRANCH_NAME}) のレビュー指摘事項" \
  --body "## 概要

PR #{PR_NUMBER} のレビューで以下の問題が見つかりました。

**対象ブランチ:** \`${BRANCH_NAME}\`

**重要:** このIssueは既存のPR #{PR_NUMBER} のブランチ \`${BRANCH_NAME}\` に対して修正を行います。
新しいブランチを作成せず、このブランチをチェックアウトして修正してください。

## 修正手順

\`\`\`bash
# 対象ブランチをチェックアウト
git fetch origin
git checkout ${BRANCH_NAME}
git pull origin ${BRANCH_NAME}

# 修正を実施
# ...

# コミット＆プッシュ
git add .
git commit -m \"fix: レビュー指摘事項の修正\"
git push origin ${BRANCH_NAME}

# PR #{PR_NUMBER} が自動的に更新されます
\`\`\`

## 問題点

### 1. {問題点1}

**詳細：** {詳細}

**修正方針：** {修正案}

### 2. {問題点2}

**詳細：** {詳細}

**修正方針：** {修正案}

## 関連PR

- #{PR_NUMBER} (ブランチ: \`${BRANCH_NAME}\`)

## チェックリスト

- [ ] ブランチ \`${BRANCH_NAME}\` をチェックアウト
- [ ] 問題点1の修正
- [ ] 問題点2の修正
- [ ] テストの追加
- [ ] コミット＆プッシュして PR #{PR_NUMBER} を更新" \
  --label "bug,priority:high" \
  --assignee "@me"

# PRにIssueへのリンクを追加
gh pr comment {PR_NUMBER} --body "修正用のIssue #{NEW_ISSUE_NUMBER} を作成しました。このIssueの完了後、再度レビューします。"
```

### 4. 承認済みPRをマージ

```bash
# 承認済みPRを確認
gh pr list --state open --json number,title,reviewDecision | jq '.[] | select(.reviewDecision == "APPROVED")'

# PRをマージ
gh pr merge {PR_NUMBER} --squash --delete-branch --body "Approved and merged. Thanks for the contribution!"

# マージ後、関連Issueをクローズ
gh issue close {ISSUE_NUMBER} --comment "PR #{PR_NUMBER} でマージ完了しました。"
```

---

## 📝 完了報告

以下の形式で報告してください：

### レビューしたPR

1. **PR #{番号}: {タイトル}**
   - アクション: Merged / Issue Created
   - 結果: {マージ完了 または Issue #{番号}を作成}

### マージしたPR

1. **PR #{番号}: {タイトル}**
   - マージ方法: Squash and Merge
   - 関連Issue: #{番号} をクローズ

### 作成したIssue（問題があった場合）

1. **Issue #{番号}: Fix: PR #{PR番号} ({ブランチ名}) のレビュー指摘事項**
   - 対象ブランチ: {ブランチ名}
   - 問題点: {要約}
   - 優先度: high
   - 修正方法: 既存のPRブランチに対して修正コミットを追加

---

## 🎯 完了基準

**重要：以下を必ず実行してください**

- [ ] 少なくとも1つのPRをレビュー
- [ ] レビューしたPRに対して **必ず以下のどちらかを実行**：
  - [ ] 問題がない → **承認してマージ**
  - [ ] 問題がある → **Issue発行**（修正内容を明記）
- [ ] レビュー内容とアクションを報告

**完了したら、このIssueをクローズしてください。**

---

## ⚠️ 重要

- **丁寧にレビューしてください**（チェックリストを活用）
- **必ずマージまたはIssue発行を実行してください**（コメントだけで終わらせない）
- **Issueには具体的な修正内容を記載してください**
- **修正Issueには必ず対象ブランチ名を明記してください**
- **新しいブランチではなく、既存のPRブランチに対して修正してください**
- **承認する前に必ず動作確認してください**
- **マージ後はブランチを削除してください**
