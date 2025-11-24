## 🧹 プロジェクト整理タスク

**今すぐ実行：**
1. 30日以上更新なしのIssueをクローズ
2. 完了したマイルストーンをクローズ
3. オープンなIssue/PRをプロジェクトボードに追加
4. このIssueをクローズ

**禁止：**
- ❌ 「推奨」だけで終わる
- ❌ 分析だけで実行しない

---

## 実行

```bash
# 1. 古いIssueをクローズ
gh issue list --state open --json number,updatedAt \
  --jq '.[] | select((.updatedAt | fromdateiso8601) < (now - 2592000)) | .number' \
  | xargs -I{} gh issue close {} --comment "30日以上更新なしのためクローズ"

# 2. 完了したマイルストーンをクローズ
gh api repos/:owner/:repo/milestones \
  --jq '.[] | select(.state=="open" and .open_issues==0) | .number' \
  | xargs -I{} gh api repos/:owner/:repo/milestones/{} -X PATCH -f state=closed

# 3. プロジェクトボードに追加
PROJ=$(gh project list --owner {OWNER} --format json | jq -r '.[0].number')
gh issue list --state open --json number \
  | jq -r '.[].number' \
  | xargs -I{} gh project item-add $PROJ --owner {OWNER} --url https://github.com/{OWNER}/{REPO}/issues/{}

# 4. このIssueをクローズ
gh issue close {THIS_ISSUE} --comment "完了"
```

**「推奨」ではなく、必ず実行してください。**
