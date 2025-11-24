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

### 3. レビューコメントを投稿

```bash
# 問題がある場合
gh pr review {PR_NUMBER} --comment --body "## レビューコメント

以下の点について修正をお願いします：

### 1. {問題点1}

{詳細}

### 2. {問題点2}

{詳細}

---

修正後、再度レビューします。"

# 承認する場合
gh pr review {PR_NUMBER} --approve --body "LGTM! 問題ありません。マージして良いと思います。

**確認した点：**
- コード品質 ✓
- テストカバレッジ ✓
- セキュリティ ✓
- パフォーマンス ✓
- ドキュメント ✓"
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
   - レビュー結果: Approved / Changes Requested
   - 主なコメント: {要約}

### マージしたPR

1. **PR #{番号}: {タイトル}**
   - マージ方法: Squash and Merge
   - 関連Issue: #{番号}

### 次回確認が必要なPR

- PR #{番号}: {タイトル} - {理由}

---

## 🎯 完了基準

- [ ] 少なくとも1つのPRをレビュー
- [ ] 承認済みPRがあればマージ
- [ ] レビュー内容を報告

**完了したら、このIssueをクローズしてください。**

---

## ⚠️ 重要

- **丁寧にレビューしてください**（チェックリストを活用）
- **建設的なコメントを書いてください**
- **承認する前に必ず動作確認してください**
- **マージ後はブランチを削除してください**
