---
name: 親Issue（複数の子Issueに分解）
about: 複数の実装タスクに分解される大きな機能
title: '[親] '
labels: 'parent'
assignees: ''
---

## 要件
<!-- 実現したい機能・目的を箇条書きで列挙 -->
-

## 子Issue分解方針
<!-- 1クラス/1メソッド粒度で分解。自動分解も可 -->
@claudeメンションで自動分解可能

## 受け入れ条件（必須）
- [ ] 全ての子Issueがクローズ
- [ ] 全ての子Issueでドキュメント追加済み
- [ ] 全ての子Issueでテスト作成・合格
- [ ] ローカル環境で動作確認完了（正常系エラーなし）

## 設定（作成後すぐ実行）
```bash
# マイルストーン設定
gh issue edit {N} --milestone "マイルストーン1: MVP - ローカル動作確認"

# プロジェクト追加
gh issue edit {N} --add-project "掲示板アプリ開発"

# ブランチ作成
BRANCH="claude/parent-issue-{N}-$(date +%Y%m%d-%H%M)"
git checkout develop && git pull
git checkout -b "$BRANCH"
git push -u origin "$BRANCH"

# Draft PR作成
gh pr create --draft --base develop --title "親: {タイトル}" --body "Closes #{N}"
```

**禁止：分析だけ、推奨だけで終わる。必ずコマンド実行。**
