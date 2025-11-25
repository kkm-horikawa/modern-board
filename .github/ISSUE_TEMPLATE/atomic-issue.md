---
name: 子Issue（atomic・実装可能）
about: 1要件・1クラス/メソッド・1テストの原子的タスク
title: '[子] '
labels: 'child,atomic,implementation'
assignees: ''
---

## 基本原則（厳守推奨）
- ✅ **1要件**（基本厳守）
- ✅ **1クラス/1メソッド**（基本だが絶対ではない）
- ✅ **1テスト**（基本だが絶対ではない）

## 親Issue
<!-- 親Issueがあれば記載 -->
#

## 要件
<!-- 1つの明確な要件を記載 -->
-

## 実装内容
<!-- 具体的なクラス/メソッド名 -->
-

## テスト観点
<!-- このIssueで確認すべきテスト -->
- [ ]

## 仕様/条件
<!-- 制約・前提条件・注意事項 -->
-

## 設定（作成後すぐ実行）
```bash
ISSUE_NUM={このIssue番号}
PARENT_BRANCH={親ブランチ名 or develop}

# マイルストーン・プロジェクト設定
gh issue edit $ISSUE_NUM --milestone "マイルストーン1: MVP - ローカル動作確認"
gh issue edit $ISSUE_NUM --add-project "掲示板アプリ開発"

# ブランチ作成
BRANCH="claude/issue-${ISSUE_NUM}-$(date +%Y%m%d-%H%M)"
git checkout "$PARENT_BRANCH" && git pull
git checkout -b "$BRANCH"
git push -u origin "$BRANCH"

# Draft PR作成
gh pr create --draft --base "$PARENT_BRANCH" --title "子: {タイトル}" --body "Closes #${ISSUE_NUM}"
```

## @claude実装指示
Draft PR・ラベル・リレーション・マイルストーン・プロジェクト設定済み前提で実装。
**禁止：分析だけ、推奨だけ。必ずコード書いてコミット・プッシュ・`gh pr ready`実行。**
