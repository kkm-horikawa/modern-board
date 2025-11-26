#!/bin/bash
# 子Issue作成 + マイルストーン・プロジェクト・ブランチ・PR設定を自動化

# エラーハンドリング設定
set -e  # エラー時に即座に終了
set -u  # 未定義変数の使用を禁止
set -o pipefail  # パイプライン内のエラーを検知

# 入力パラメータの検証
if [ $# -ne 3 ]; then
  echo "Error: Invalid number of arguments" >&2
  echo "Usage: $0 <PARENT_ISSUE> <TITLE> <BODY>" >&2
  exit 1
fi

PARENT_ISSUE=$1
TITLE=$2
BODY=$3

# 親Issueの存在確認
if ! gh issue view "$PARENT_ISSUE" &>/dev/null; then
  echo "Error: Parent issue #$PARENT_ISSUE does not exist" >&2
  exit 1
fi

# developブランチの存在確認
if ! git rev-parse --verify develop &>/dev/null; then
  echo "Error: develop branch does not exist" >&2
  exit 1
fi

# 親のマイルストーン・プロジェクトを取得
MILESTONE=$(gh issue view "$PARENT_ISSUE" --json milestone --jq '.milestone.title')
PROJECT=$(gh issue view "$PARENT_ISSUE" --json projectItems --jq '.projectItems[0].project.title')

# 子Issue作成
CHILD_URL=$(gh issue create \
  --title "$TITLE" \
  --body "$BODY" \
  --label "child,automation,implementation" \
  --milestone "$MILESTONE")

CHILD_NUM=$(echo "$CHILD_URL" | sed 's|.*/||')

# プロジェクト追加
[ -n "$PROJECT" ] && gh issue edit "$CHILD_NUM" --add-project "$PROJECT"

# ブランチ作成
PARENT_BRANCH="claude/parent-issue-${PARENT_ISSUE}-$(date +%Y%m%d-%H%M)"
CHILD_BRANCH="claude/child-issue-${CHILD_NUM}-$(date +%Y%m%d-%H%M)"

# developブランチに切り替えて最新を取得
if ! git checkout develop; then
  echo "Error: Failed to checkout develop branch" >&2
  exit 1
fi

if ! git pull; then
  echo "Error: Failed to pull latest changes from develop" >&2
  exit 1
fi

# 親ブランチの作成または切り替え
if ! git checkout -b "$PARENT_BRANCH" 2>/dev/null; then
  if ! git checkout "$PARENT_BRANCH"; then
    echo "Error: Failed to create or checkout parent branch" >&2
    exit 1
  fi
fi

# 親ブランチをプッシュ（既に存在する場合はエラーを無視）
git push origin "$PARENT_BRANCH" 2>/dev/null || true

# 親ブランチに確実に切り替え
git checkout "$PARENT_BRANCH"

# 子ブランチを作成
if ! git checkout -b "$CHILD_BRANCH"; then
  echo "Error: Failed to create child branch" >&2
  exit 1
fi

# 子ブランチをプッシュ
if ! git push -u origin "$CHILD_BRANCH"; then
  echo "Error: Failed to push child branch" >&2
  exit 1
fi

# Draft PR作成
gh pr create --draft \
  --head "$CHILD_BRANCH" \
  --base "$PARENT_BRANCH" \
  --title "$TITLE" \
  --body "Closes #${CHILD_NUM}

親Issue: #${PARENT_ISSUE}

$BODY"

echo "$CHILD_NUM"
