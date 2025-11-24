## 🔍 PRレビュー・マージタスク

**今すぐ実行：**
1. Ready for ReviewのPRを1つ選ぶ
2. レビューする
3. **必ず**以下のどちらかを実行：
   - 問題なし → **マージする**
   - 問題あり → **修正Issueを作成する**

**禁止：**
- ❌ コメントだけで終わる
- ❌ 「推奨」だけで実行しない
- ❌ 判断を保留する

---

## 実行

```bash
# PRを選ぶ
gh pr list --state open --json number,title,isDraft | jq '.[] | select(.isDraft == false)'

# レビュー（コード品質、テスト、セキュリティを確認）
gh pr view {N}
gh pr diff {N}

# 判断して必ず実行
# A. 問題なし → マージ
gh pr review {N} --approve --body "LGTM"
gh pr merge {N} --squash --delete-branch

# B. 問題あり → 修正Issue作成
BRANCH=$(gh pr view {N} --json headRefName -q .headRefName)
gh issue create \
  --title "Fix: PR #{N} (${BRANCH}) の修正" \
  --body "PR #{N} に問題。ブランチ ${BRANCH} に対して修正してください。

問題点:
- {具体的な問題}

修正手順:
\`\`\`bash
git checkout ${BRANCH}
# 修正
git push
\`\`\`" \
  --label "bug,priority:high"

# このIssueをクローズ
gh issue close {THIS_ISSUE} --comment "完了"
```

**必ずマージまたはIssue作成を実行してください。**
