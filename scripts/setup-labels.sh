#!/bin/bash

# GitHub Labels Setup Script
# このスクリプトは、Claude自動化ワークフローに必要なラベルを作成します

set -e

echo "🏷️  GitHub Labelsをセットアップします..."

# ラベルが存在しない場合のみ作成
create_label_if_not_exists() {
  local name=$1
  local description=$2
  local color=$3

  if gh label list --json name --jq '.[].name' | grep -q "^${name}$"; then
    echo "✓ ラベル '${name}' は既に存在します"
  else
    echo "+ ラベル '${name}' を作成中..."
    gh label create "${name}" --description "${description}" --color "${color}"
  fi
}

# 自動化関連ラベル
create_label_if_not_exists "automation" "自動化によって作成されたIssue/PR" "0E8A16"
create_label_if_not_exists "implementation" "機能実装タスク" "1D76DB"
create_label_if_not_exists "review" "レビュータスク" "FBCA04"
create_label_if_not_exists "issue-management" "Issue管理タスク" "D93F0B"
create_label_if_not_exists "organization" "プロジェクト整理タスク" "0052CC"
create_label_if_not_exists "cleanup" "ブランチ整理タスク" "5319E7"
create_label_if_not_exists "decomposition" "Issue分解タスク" "9C27B0"
create_label_if_not_exists "documentation" "ドキュメント関連タスク" "0075CA"
create_label_if_not_exists "documentation-org" "ドキュメント整理タスク" "1E90FF"

# Issue粒度管理ラベル
create_label_if_not_exists "atomic" "分解不要な最小単位Issue" "00C851"
create_label_if_not_exists "parent" "子Issueを持つ親Issue" "8B4789"
create_label_if_not_exists "child" "親Issueの一部である子Issue" "C5DEF5"

# 優先度ラベル
create_label_if_not_exists "priority:critical" "最優先で対応が必要" "B60205"
create_label_if_not_exists "priority:high" "優先度が高い" "D93F0B"
create_label_if_not_exists "priority:medium" "通常の優先度" "FBCA04"
create_label_if_not_exists "priority:low" "優先度が低い" "0E8A16"

# その他の有用なラベル
create_label_if_not_exists "bug" "バグ報告" "D73A4A"
create_label_if_not_exists "enhancement" "新機能または改善" "A2EEEF"

echo ""
echo "✅ ラベルのセットアップが完了しました！"
