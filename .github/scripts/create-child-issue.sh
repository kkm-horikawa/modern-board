#!/bin/bash
# 子Issue作成 + マイルストーン・プロジェクト・ブランチ・PR設定を自動化

PARENT_ISSUE=$1
TITLE=$2
BODY=$3

# 親のマイルストーン・プロジェクトを取得
MILESTONE=$(gh issue view $PARENT_ISSUE --json milestone --jq '.milestone.title')
PROJECT=$(gh issue view $PARENT_ISSUE --json projectItems --jq '.projectItems[0].project.title')

# 子Issue作成
CHILD_URL=$(gh issue create \
  --title "$TITLE" \
  --body "$BODY" \
  --label "child,automation,implementation" \
  --milestone "$MILESTONE")

CHILD_NUM=$(echo $CHILD_URL | sed 's|.*/||')

# プロジェクト追加
[ -n "$PROJECT" ] && gh issue edit $CHILD_NUM --add-project "$PROJECT"

# ブランチ作成
PARENT_BRANCH="claude/parent-issue-${PARENT_ISSUE}-$(date +%Y%m%d-%H%M)"
CHILD_BRANCH="claude/child-issue-${CHILD_NUM}-$(date +%Y%m%d-%H%M)"

git checkout develop && git pull
git checkout -b "$PARENT_BRANCH" 2>/dev/null || git checkout "$PARENT_BRANCH"
git push origin "$PARENT_BRANCH" 2>/dev/null || true
git checkout "$PARENT_BRANCH"
git checkout -b "$CHILD_BRANCH"
git push -u origin "$CHILD_BRANCH"

# Draft PR作成
gh pr create --draft \
  --head "$CHILD_BRANCH" \
  --base "$PARENT_BRANCH" \
  --title "$TITLE" \
  --body "Closes #${CHILD_NUM}

親Issue: #${PARENT_ISSUE}

$BODY"

echo $CHILD_NUM
