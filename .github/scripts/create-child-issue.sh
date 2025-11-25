#!/bin/bash
# 子Issue作成 + マイルストーン・プロジェクト・ブランチ・PR設定を自動化
set -e  # エラー時に停止

PARENT_ISSUE=$1
TITLE=$2
BODY=$3

# 引数チェック
if [ -z "$PARENT_ISSUE" ] || [ -z "$TITLE" ]; then
  echo "Error: Missing required arguments"
  echo "Usage: $0 <parent_issue> <title> [body]"
  exit 1
fi

# developブランチの存在チェック
if ! git rev-parse --verify develop >/dev/null 2>&1; then
  echo "Error: develop branch does not exist"
  exit 1
fi

# ghコマンドの存在チェック
if ! command -v gh >/dev/null 2>&1; then
  echo "Error: gh command not found. Please install GitHub CLI"
  exit 1
fi

# 親のマイルストーン・プロジェクトを取得
MILESTONE=$(gh issue view $PARENT_ISSUE --json milestone --jq '.milestone.title // empty')
PROJECT=$(gh issue view $PARENT_ISSUE --json projectItems --jq '.projectItems[0].project.title // empty')

# 子Issue作成
if [ -n "$MILESTONE" ]; then
  CHILD_URL=$(gh issue create \
    --title "$TITLE" \
    --body "$BODY" \
    --label "child,automation,implementation" \
    --milestone "$MILESTONE")
else
  echo "Warning: No milestone found on parent issue, creating child issue without milestone"
  CHILD_URL=$(gh issue create \
    --title "$TITLE" \
    --body "$BODY" \
    --label "child,automation,implementation")
fi

CHILD_NUM=$(echo "$CHILD_URL" | sed 's|.*/||')

# プロジェクト追加
[ -n "$PROJECT" ] && gh issue edit $CHILD_NUM --add-project "$PROJECT"

# ブランチ作成（環境非依存の日付フォーマット）
TIMESTAMP=$(date -u +%Y%m%d-%H%M)
PARENT_BRANCH="claude/parent-issue-${PARENT_ISSUE}-${TIMESTAMP}"
CHILD_BRANCH="claude/child-issue-${CHILD_NUM}-${TIMESTAMP}"

# developブランチに移動して最新を取得
echo "Checking out develop branch..."
if ! git checkout develop; then
  echo "Error: Failed to checkout develop branch"
  exit 1
fi

if ! git pull; then
  echo "Error: Failed to pull latest changes from develop"
  exit 1
fi

# 親ブランチの作成または切り替え
echo "Creating or checking out parent branch: $PARENT_BRANCH"
if git rev-parse --verify "$PARENT_BRANCH" >/dev/null 2>&1; then
  git checkout "$PARENT_BRANCH"
else
  git checkout -b "$PARENT_BRANCH"
  git push -u origin "$PARENT_BRANCH"
fi

# 子ブランチの作成
echo "Creating child branch: $CHILD_BRANCH"
if ! git checkout -b "$CHILD_BRANCH"; then
  echo "Error: Failed to create child branch"
  exit 1
fi

if ! git push -u origin "$CHILD_BRANCH"; then
  echo "Error: Failed to push child branch to remote"
  exit 1
fi

# Draft PR作成
echo "Creating draft PR..."
if ! gh pr create --draft \
  --head "$CHILD_BRANCH" \
  --base "$PARENT_BRANCH" \
  --title "$TITLE" \
  --body "Closes #${CHILD_NUM}

親Issue: #${PARENT_ISSUE}

$BODY"; then
  echo "Error: Failed to create draft PR"
  exit 1
fi

echo "Successfully created child issue #${CHILD_NUM}"
echo "$CHILD_NUM"
