## 🗑️ ブランチ整理タスク

**今すぐ実行：**
1. マージ済みブランチを削除
2. PRが存在しない古いブランチを削除または Draft PR作成
3. このIssueをクローズ

**禁止：**
- ❌ 分析だけで終わる
- ❌ 削除を「推奨」だけで実行しない

---

## 実行

```bash
# 1. マージ済みブランチを削除
gh api repos/:owner/:repo/branches --jq '.[] | select(.protected == false) | .name' | while read branch; do
  [[ "$branch" =~ ^(main|master|develop)$ ]] && continue
  PR_STATE=$(gh pr list --head "$branch" --state all --json mergedAt --jq '.[0].mergedAt')
  [[ "$PR_STATE" != "null" ]] && git push origin --delete "$branch"
done

# 2. PRが存在しないブランチを整理
git fetch --all --prune
gh api repos/:owner/:repo/branches --jq '.[] | select(.protected == false) | .name' | while read branch; do
  [[ "$branch" =~ ^(main|master|develop)$ ]] && continue
  PR_COUNT=$(gh pr list --head "$branch" --state all --json number | jq 'length')

  if [ "$PR_COUNT" -eq 0 ]; then
    DAYS=$((($(date +%s) - $(date -d "$(gh api repos/:owner/:repo/branches/$branch --jq '.commit.commit.author.date')" +%s)) / 86400))
    COMMITS=$(git rev-list --count origin/develop..origin/$branch 2>/dev/null || echo 0)

    # 判断基準
    if [ "$DAYS" -gt 14 ] || ([ "$DAYS" -gt 30 ] && [ "$COMMITS" -le 2 ]); then
      git push origin --delete "$branch"  # 削除
    elif [ "$DAYS" -le 7 ] && [ "$COMMITS" -gt 0 ]; then
      gh pr create --head "$branch" --base develop --draft  # Draft PR作成
    fi
  fi
done

# 3. このIssueをクローズ
gh issue close {THIS_ISSUE} --comment "完了"
```

**必ず削除またはDraft PR作成を実行してください。**
