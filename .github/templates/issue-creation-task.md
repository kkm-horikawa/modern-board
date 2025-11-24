## 📝 新規Issue作成タスク

**今すぐ実行：**
1. 最近のマージ済みPRを3つ確認
2. バグ・改善点を見つける
3. 最低2つのIssueを作成
4. このIssueをクローズ

**禁止：**
- ❌ 分析だけで終わる
- ❌ Issue作成数が0または1

---

## 実行

```bash
# マージ済みPRを確認
gh pr list --state merged --limit 10

# 各PRを確認してバグ・改善点を探す
gh pr view {N}
gh pr diff {N}

# Issue作成（最低2つ）
gh issue create \
  --title "Bug: {問題}" \
  --body "PR #{N} で以下の問題を発見。{詳細}" \
  --label "bug,priority:high"

gh issue create \
  --title "Enhancement: {改善}" \
  --body "PR #{N} で以下の改善が可能。{詳細}" \
  --label "enhancement,priority:medium"

# このIssueをクローズ
gh issue close {THIS_ISSUE} --comment "2つのIssueを作成"
```

**最低2つのIssueを必ず作成してください。**
