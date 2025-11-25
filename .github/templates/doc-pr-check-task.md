## 📝 PR #{PR_NUMBER} のドキュメントチェック

**今すぐ実行：**
1. PR #{PR_NUMBER} の変更内容を確認
2. ドキュメント更新が含まれているか判断
3. 必要なのに含まれていない → サブIssue作成
4. 含まれている or 不要 → PRにコメントして終了
5. このIssueをクローズする

**禁止：**
- ❌ 分析だけで終わる
- ❌ 判断を保留する

---

## ドキュメント必要性の判断基準

**必要**:
- 新機能追加
- APIエンドポイント変更
- アーキテクチャ変更
- 環境構築手順変更

**不要**:
- バグ修正のみ
- リファクタリングのみ
- テスト追加のみ

---

## 実行

```bash
# 1. PRの変更内容を確認
gh pr view {PR_NUMBER}
gh pr diff {PR_NUMBER}

# 2. ドキュメント更新が含まれているかチェック
DOCS_CHANGED=$(gh pr diff {PR_NUMBER} --name-only | grep -E '^docs/.*\.md$' | wc -l)

# 判断A: ドキュメント更新済み or 不要
if [ "$DOCS_CHANGED" -gt 0 ] || [ 不要と判断 ]; then
  gh pr comment {PR_NUMBER} --body "✅ ドキュメントチェック完了"
  gh issue close {THIS_ISSUE} --comment "完了"
  exit 0
fi

# 判断B: ドキュメント更新が必要 → サブIssue作成
PR_TITLE=$(gh pr view {PR_NUMBER} --json title -q .title)
PR_BRANCH=$(gh pr view {PR_NUMBER} --json headRefName -q .headRefName)

# 必要なドキュメント種類を判断
# 新機能 → features, API変更 → development, 環境構築 → development, 要件 → requirements

DOC_TYPE="features"  # または development/requirements/design

gh issue create \
  --title "DOC: PR #{PR_NUMBER} - ${PR_TITLE}" \
  --body "## 📝 PR #{PR_NUMBER} のドキュメント作成

**対象PR**: #{PR_NUMBER}
**ブランチ**: \`${PR_BRANCH}\`
**ドキュメント種類**: \`docs/${DOC_TYPE}/\`

**今すぐ実行：**
1. PR #{PR_NUMBER} の変更内容を確認
2. \`docs/${DOC_TYPE}/{name}.md\` を作成
3. \`docs/README.md\` を更新
4. ブランチ \`${PR_BRANCH}\` にコミット・プッシュ
5. このIssueをクローズ

**ドキュメントルール：**
- **300行以内**（超えたら分割）
- **TL;DR必須**（冒頭に要約セクション）
- **最終更新日**：\`最終更新: $(date +%Y-%m-%d)\`
- **既存との重複確認**：\`docs/README.md\` で確認

**テンプレート：**
\`\`\`markdown
# {タイトル}

## TL;DR
{2-3行の要約}

## 概要
{詳細説明}

## 使い方
{具体例}

---
最終更新: $(date +%Y-%m-%d)
\`\`\`" \
  --label "automation,documentation,child" \
  --assignee "@me"

DOC_ISSUE=\$(gh issue list --label "documentation" --limit 1 --json number -q '.[0].number')

# PRにコメント
gh pr comment {PR_NUMBER} --body "📝 ドキュメント作成が必要です: #${DOC_ISSUE}

このPRをマージする前に、ドキュメントIssue #${DOC_ISSUE} をクローズしてください。"

# このIssueをクローズ
gh issue close {THIS_ISSUE} --comment "完了"
```

**必ずサブIssue作成またはPRコメントを実行してください。**
