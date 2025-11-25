## 🚀 機能実装タスク

**今すぐ実行：**
1. 優先度の高いIssueを1つ選ぶ
2. ブランチ作成 + Draft PR作成（計画）
3. 実装 + テスト
4. Ready for Review
5. 完了

**禁止：**
- ❌ 分析だけで終わる
- ❌ 複数のIssueに手を出す
- ❌ Draft PRのまま放置

---

## 実行

```bash
# 1. Issue選択（優先順位: critical → bug+high → high）
TARGET=$(gh issue list --state open --label "priority:critical" --limit 1 --json number --jq '.[0].number')
[ -z "$TARGET" ] && TARGET=$(gh issue list --state open --label "bug,priority:high" --limit 1 --json number --jq '.[0].number')
[ -z "$TARGET" ] && TARGET=$(gh issue list --state open --label "priority:high" --limit 1 --json number --jq '.[0].number')

gh issue view $TARGET

# 2. ブランチ + Draft PR作成
git checkout develop && git pull
BRANCH="claude/issue-${TARGET}-$(date +%Y%m%d-%H%M)"
git checkout -b "$BRANCH"
git commit --allow-empty -m "draft: Issue #${TARGET} 実装開始"
git push origin HEAD

gh pr create --draft \
  --title "WIP: Issue #${TARGET}" \
  --body "Closes #${TARGET}

## 実装計画
..." \
  --base develop

# 3. 実装 + テスト
# ... コードを書く + テストを書く ...
git add . && git commit -m "feat: Issue #${TARGET}"
git push

# 4. Ready for Review（必須）
gh pr ready

# 5. 完了
gh issue close {THIS_ISSUE} --comment "完了: Issue #${TARGET} 実装"
```

**必ず `gh pr ready` を実行。Draftのまま放置禁止。**
**PR本文に `Closes #N` で自動Development紐付け。**
