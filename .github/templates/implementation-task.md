## 🚀 機能実装タスク

**今すぐ実行：**
1. 優先度の高いIssueを1つ選ぶ
2. 実装してテストを書く
3. PRを作成して **Ready for Review** にする
4. このIssueをクローズする

**禁止：**
- ❌ 分析だけで終わる
- ❌ 複数のIssueに手を出す
- ❌ Draft PRのまま放置する

---

## 実行

```bash
# Issueを選ぶ
gh issue list --state open --label "priority:critical,priority:high" --limit 5

# 実装
git checkout develop && git pull
git checkout -b claude/issue-{N}-$(date +%Y%m%d-%H%M)
# ... コードを書く + テストを書く ...
git add . && git commit -m "feat: Issue #{N}"
git push origin HEAD

# PR作成して Ready for Review にする
gh pr create --draft --title "feat: Issue #{N}" --base develop
gh pr ready  # 必ず実行

# このIssueをクローズ
gh issue close {THIS_ISSUE} --comment "完了"
```

**必ず `gh pr ready` を実行してください。Draft のままにしないでください。**
