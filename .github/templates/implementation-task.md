## 🚀 機能実装タスク

**今すぐ実行：**
1. 優先度の高いIssueを1つ選ぶ
2. **Draft PR作成（計画だけ）**
3. 実装してテストを書く
4. **Ready for Review** にする
5. このIssueをクローズする

**禁止：**
- ❌ 分析だけで終わる
- ❌ 複数のIssueに手を出す
- ❌ Draft PRのまま放置する

---

## 実行

```bash
# 1. Issueを選ぶ（優先順位: critical → bug+high → high）
gh issue list --state open --label "priority:critical" --limit 3
gh issue list --state open --label "bug,priority:high" --limit 3
gh issue list --state open --label "priority:high" --limit 3

# 2. ブランチ作成してすぐDraft PR作成
git checkout develop && git pull
git checkout -b claude/issue-{N}-$(date +%Y%m%d-%H%M)
git commit --allow-empty -m "draft: Issue #{N} 実装開始"
git push origin HEAD
gh pr create --draft --title "WIP: Issue #{N}" --body "実装計画: ..." --base develop

# 3. 実装
# ... コードを書く + テストを書く ...
git add . && git commit -m "feat: Issue #{N}"
git push

# 4. Ready for Review にする
gh pr ready  # 必ず実行

# このIssueをクローズ
gh issue close {THIS_ISSUE} --comment "完了"
```

**必ず `gh pr ready` を実行してください。Draft のままにしないでください。**
