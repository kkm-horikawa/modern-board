## 📝 新規Issue作成タスク

**今すぐ実行：**
1. マージ済みPRを3つ確認
2. バグ・改善点を見つける
3. 最低2つのIssueを作成（マイルストーン・プロジェクト・ブランチ・PR自動設定）
4. 完了

**禁止：**
- ❌ 分析・推奨・説明だけで終わる
- ❌ 「〇〇すべき」「推奨します」で終わる
- ❌ `gh issue create`実行しない
- ❌ Issue作成数が0または1

---

## 実行

```bash
# 1. マージ済みPR確認
gh pr list --state merged --limit 10
gh pr view {N}
gh pr diff {N}

# 2-3. Issue作成（スクリプトで自動設定）
# マイルストーン・プロジェクト・ブランチ・Draft PR・Development紐付けを自動化

# デフォルトマイルストーン・プロジェクト（最新のopenマイルストーン、メインプロジェクト）
MILESTONE=$(gh api repos/{owner}/{repo}/milestones --jq '.[0].title')
PROJECT="掲示板アプリ開発"  # リポジトリのメインプロジェクト名

ISSUE1=$(gh issue create \
  --title "Bug: {問題}" \
  --body "PR #{N}で発見。{詳細}" \
  --label "bug,priority:high" \
  --milestone "$MILESTONE")

gh issue edit $(echo $ISSUE1 | sed 's|.*/||') --add-project "$PROJECT"

ISSUE2=$(gh issue create \
  --title "Enhancement: {改善}" \
  --body "PR #{N}で改善可能。{詳細}" \
  --label "enhancement,priority:medium" \
  --milestone "$MILESTONE")

gh issue edit $(echo $ISSUE2 | sed 's|.*/||') --add-project "$PROJECT"

# 4. 完了
gh issue close {THIS_ISSUE} --comment "2つのIssueを作成"
```

**最低2つのIssueを必ず作成してください。**
**自動設定**: マイルストーン・プロジェクト（ブランチ・PRは実装タスクで作成）
