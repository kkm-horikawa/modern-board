## 🚀 機能実装タスク

**目的：優先度の高いIssueを1つ選択して、実装を完了させる**

---

## 📋 実行手順

### 1. 実装すべきIssueを選択

```bash
# 優先度の高いIssueを確認
gh issue list --state open --label "priority:high" --json number,title,labels
gh issue list --state open --label "priority:critical" --json number,title,labels

# Draft PRが停滞しているものを確認
gh pr list --state open --draft --json number,title,updatedAt
```

**選択基準（優先順位順）：**
1. `priority:critical` ラベルのIssue
2. `priority:high` ラベルで実装が必要なIssue
3. 48時間以上更新されていないDraft PR
4. `priority:medium` で依存関係がクリアなIssue

**1つだけ選択してください。**

### 2. 実装を完了させる

選択したIssueに対して実装を完了させてください：

#### A. 新規実装の場合

```bash
# ブランチ作成
git checkout develop
git pull origin develop
git checkout -b claude/issue-{ISSUE_NUMBER}-$(date +%Y%m%d-%H%M)

# コードを実装
# - 機能コードを書く
# - テストコードを書く
# - ドキュメントを更新

# コミット & プッシュ
git add .
git commit -m "feat: Issue #{ISSUE_NUMBER} の実装

- 実装内容を簡潔に記載

Closes #{ISSUE_NUMBER}"
git push origin HEAD

# Draft PR作成
gh pr create --draft \
  --title "feat: Issue #{ISSUE_NUMBER} タイトル" \
  --body "## 概要

Issue #{ISSUE_NUMBER} の実装

## 変更内容

- 変更1
- 変更2

## テスト

- [ ] ユニットテスト追加
- [ ] 動作確認完了

Closes #{ISSUE_NUMBER}" \
  --base develop

# Ready for Review
gh pr ready {PR_NUMBER}
```

#### B. 既存Draft PRの続き

```bash
# PRをチェックアウト
gh pr checkout {PR_NUMBER}

# 実装を進める
# - コードを追加・修正
# - テストを追加
# - レビューコメントに対応

# コミット & プッシュ
git add .
git commit -m "feat: 追加実装・修正"
git push

# Ready for Review
gh pr ready {PR_NUMBER}
```

---

## 📝 完了報告

実装が完了したら、以下の形式で報告してください：

### 実装したIssue

**Issue #{番号}: {タイトル}**
- 実装内容: {何を実装したか}
- PR: #{PR番号}
- ステータス: Draft / Ready for Review
- ファイル変更: {変更したファイル数}行追加、{削除行数}行削除

### 次回推奨タスク

- Issue #{番号}: {タイトル} （{優先度}）

---

## 🎯 完了基準

- [ ] 1つのIssueに対して実装を完了
- [ ] Draft PR作成 または Ready for Reviewに変更
- [ ] テストコードを追加
- [ ] 実装内容を報告

**完了したら、このIssueをクローズしてください。**

---

## ⚠️ 重要

- **1つのIssueに集中してください**（複数に手を出さない）
- **実装まで完了させてください**（分析だけで終わらない）
- **テストを必ず書いてください**
- **コードレビュー可能な状態にしてください**
