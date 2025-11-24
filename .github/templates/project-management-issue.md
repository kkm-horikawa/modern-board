## 🤖 自動プロジェクト管理・実装タスク

**このタスクの目的：プロジェクトを実際に進行させること**

分析や報告だけでなく、**実際にコードを書いて、機能を実装してください。**

---

## 📋 実行手順

### 1. 現在の状況を把握

```bash
# オープンなIssueを確認
gh issue list --state open --json number,title,labels,createdAt

# オープンなPRを確認
gh pr list --state open --json number,title,isDraft

# 分析スクリプトを実行
python3 .github/scripts/analyze_project.py
```

### 2. 最優先で実装すべきIssueを選択

以下の基準で **1つのIssue** を選択してください：

**優先順位:**
1. **CRITICAL** ラベルのIssue
2. **priority:high** + 実装が必要なIssue
3. **Draft PR** が停滞しているもの（48時間以上更新なし）
4. **priority:medium** で実装が必要なIssue

**選択基準:**
- 実装が必要なもの（ドキュメント作成、コード実装、テスト実装など）
- 依存関係がクリアで、今すぐ着手できるもの
- マージ待ちのPRがあれば、そのレビュー・マージを優先

### 3. 実装を開始

選択したIssueに対して、**実際に実装を完了させてください：**

#### A. 新規実装の場合

```bash
# 1. ブランチ作成
git checkout -b claude/issue-{ISSUE_NUMBER}-{YYYYMMDD}-{HHMM}

# 2. コードを実装
# - 機能コードを書く
# - テストコードを書く
# - ドキュメントを更新

# 3. コミット
git add .
git commit -m "feat: Issue #{ISSUE_NUMBER} の実装"

# 4. プッシュ
git push origin HEAD

# 5. Draft PRを作成
gh pr create --draft \
  --title "feat: Issue #{ISSUE_NUMBER} タイトル" \
  --body "Closes #{ISSUE_NUMBER}" \
  --base develop

# 6. PRに実装内容をコメント
gh pr comment {PR_NUMBER} --body "実装完了しました。レビューをお願いします。"

# 7. Draft → Ready for Review
gh pr ready {PR_NUMBER}
```

#### B. 既存Draft PRの続きの場合

```bash
# 1. ブランチをチェックアウト
gh pr checkout {PR_NUMBER}

# 2. 実装を進める
# - コードを追加・修正
# - テストを追加
# - レビューコメントに対応

# 3. コミット & プッシュ
git add .
git commit -m "feat: 追加実装・修正"
git push

# 4. 完了したらReady for Review
gh pr ready {PR_NUMBER}
```

#### C. レビュー待ちPRがある場合

```bash
# PRをマージ（承認済みの場合）
gh pr merge {PR_NUMBER} --squash --delete-branch

# マージ後、Issueをクローズ
gh issue close {ISSUE_NUMBER} --comment "PR #{PR_NUMBER} でマージ完了"
```

### 4. マージ済みPRをチェックして新しいIssueを作成

実装が完了したら、**マージ済みPRを分析して改善サイクルを回してください：**

```bash
# 最近マージされたPRを確認（過去7日間）
gh pr list --state merged --limit 5 --json number,title,mergedAt

# 各マージ済みPRについて：
# 1. 変更内容を確認
gh pr view {PR_NUMBER} --json files,additions,deletions

# 2. コードをレビュー
#    - バグの可能性はないか？
#    - パフォーマンス問題はないか？
#    - セキュリティ問題はないか？
#    - テストは十分か？
#    - ドキュメントは更新されているか？

# 3. 問題があればBug Issueを作成
gh issue create \
  --title "Bug: PR #{PR_NUMBER} の{問題の要約}" \
  --body "PR #{PR_NUMBER} でマージされた実装に以下の問題があります：..." \
  --label "bug,priority:high"

# 4. 改善提案があればEnhancement Issueを作成
gh issue create \
  --title "Enhancement: {改善内容}" \
  --body "PR #{PR_NUMBER} の実装に対する改善提案..." \
  --label "enhancement,priority:medium"

# 5. 次のマイルストーンのタスクを提案
#    - 現在のマイルストーンの進捗を確認
#    - 完了している場合は次のマイルストーンのタスクを作成
```

**重要：**
- マージ済みPRは必ずチェックする
- 少なくとも1つは新しいIssueを作成する（改善提案でも良い）
- プロジェクトが継続的に進むように、次のタスクを用意する

### 5. 次のタスクを見つける

実装と改善サイクルが完了したら、**手順1に戻って次のタスクを実行してください。**

**時間が許す限り、複数のIssueに対して実装を進めてください。**

---

## 📝 実行後の報告

以下の形式で報告してください：

### 実装したIssue

1. **Issue #{番号}: {タイトル}**
   - 実装内容: {何を実装したか}
   - PR: #{PR番号}
   - ステータス: Draft / Ready for Review / Merged
   - 所要時間: {大体の時間}

2. **Issue #{番号}: {タイトル}**
   - ...

### 作成した新しいIssue

1. **Issue #{番号}: {タイトル}** （{Bug/Enhancement}）
   - 理由: {なぜ作成したか}
   - 対象PR: #{PR番号}
   - 優先度: {priority}

### 次回の推奨タスク

- Issue #{番号}: {タイトル} （{優先度}）

---

## 🎯 完了基準

**重要：以下をすべて達成してください**

- [ ] 少なくとも **1つのIssueに対して実装を完了**（Draft PR作成またはコード実装）
- [ ] マージ済みPRをチェックして **少なくとも1つの新しいIssueを作成**
- [ ] 実装内容と新規Issue作成を報告
- [ ] 次回の推奨タスクを記載

**実装と改善サイクルが完了したら、このIssueをクローズしてください。**

---

## ⚠️ 重要な注意事項

1. **「分析だけ」「チェックだけ」で終わらないでください**
   - 必ず実装まで完了させる
   - コードを書く、テストを書く、PRを作成する

2. **「次回推奨アクション」だけ書いて終わらないでください**
   - 今すぐ実装する
   - 次回ではなく、今回実装する

3. **新しいIssueを必ず作成してください**
   - マージ済みPRから改善点を見つける
   - 次のタスクを用意する
   - プロジェクトが継続的に進むようにする

4. **複数のIssueを進めてください**
   - 時間が許す限り、2つ以上のIssueに着手
   - 1つだけで満足しない

5. **実装の質を保ってください**
   - テストを書く
   - ドキュメントを更新する
   - レビュアブルなコードを書く
