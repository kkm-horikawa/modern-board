## 🤖 自動プロジェクト管理タスク

プロジェクト全体を分析し、優先順位に基づいてアクションを実行してください。

---

## 🔧 Step 0: 初回セットアップチェック（最優先）

**チェック項目:**
```bash
# プロジェクト存在確認
gh project list --owner @me | grep "プロジェクト名"

# マイルストーン確認（5件必要）
gh api repos/:owner/:repo/milestones | jq 'length'

# ラベル確認
gh label list | grep "priority:"
```

**セットアップが必要な場合:**
1. `.github/templates/project-setup.md` を読む
2. プロジェクト/マイルストーン/ラベル/初期Issueを作成
3. 完了報告後、通常の分析へ進む

---

## 📊 分析と実行

### 1. PR確認
```bash
gh pr list --state open  # Draft PRがあるIssueには着手しない

# PRが存在しないブランチを検出
git fetch origin
git branch -r | grep -v "HEAD\|master\|main\|develop" | while read branch; do
  branch_name=${branch#origin/}
  if ! gh pr list --state all --head $branch_name --json number | jq -e '. | length > 0' > /dev/null; then
    echo "PR未作成: $branch_name"
  fi
done
```
- **PR未作成のブランチがあれば、PRを作成**
- レビューが必要なPRを特定してレビュー実行
- レビュー済み・CI通過済みのPRは `gh pr merge` でマージ

### 2. Issue優先順位
```bash
gh issue list --label "priority:critical"
gh issue list --label "bug"
gh issue list --milestone "マイルストーン名"
```
- Critical/High優先度のIssueを特定
- 各マイルストーンの進捗を確認

### 3. CI/CD健全性
```bash
gh run list --limit 10
```
- ビルド失敗やエラーを確認

### 4. 停滞タスク検出
- `@claude` メンション未応答のIssue/PR
- 48時間以上更新されていないDraft PR
- 72時間以上放置されているレビュー待ちPR

→ 停滞タスクには再度 `@claude` をメンション

### 5. アクション実行

**優先順位:**
1. **Critical**: バグ修正、ブロッカー解消
2. **High**: 停滞タスク再実行、PRレビュー
3. **Medium**: 現在のマイルストーン進行
4. **Low**: ドキュメント改善

**実行可能なアクション:**
- **PR未作成のブランチのPR作成**（実装完了しているがPRがない場合）
- Issue実装（Draft PRが存在しないことを確認後）
- PRレビュー（Approve/Request Changes/Comment）
- PRマージ（レビュー済み・CI通過済み）
- 新規Issue作成
- マイルストーン割り当て
- プロジェクトボード更新

**重要: Issue実装時は必ずDraft PR作成から開始**
```bash
git checkout -b feature/issue-XX
git commit --allow-empty -m "WIP: Issue #XX"
git push origin feature/issue-XX
gh pr create --draft --title "WIP: Issue #XX" --body "Closes #XX" --base develop
# 実装後: gh pr ready
```

---

## 📝 実行後の報告

**プロジェクト状況:**
- 各マイルストーン進捗（X/Y完了）
- オープンPR数、バグ数

**実行アクション:**
1. [種別] #番号 - 概要と結果

**検出した問題:**
- 問題と対応

**次回推奨アクション:**
- 次に取り組むべき内容

---

## 🎯 完了基準

- [ ] 全分析項目を実行
- [ ] 少なくとも1つのアクションを実行
- [ ] 報告を記載

**完了後は自動的にこのIssueをクローズしてください。**
