## 🗑️ ブランチ整理タスク

**目的：マージ済みブランチと孤立ブランチを整理する**

---

## 📋 実行手順

### 1. マージ済みブランチの削除

```bash
# マージ済みのブランチを確認して削除
gh api repos/:owner/:repo/branches --jq '.[] | select(.protected == false) | .name' | while read branch; do
  # main/master/developは除外
  if [[ "$branch" == "main" || "$branch" == "master" || "$branch" == "develop" ]]; then
    continue
  fi

  # PRがマージ済みか確認
  PR_STATE=$(gh pr list --head "$branch" --state all --json state,mergedAt --jq '.[0] | select(.mergedAt != null) | .state')

  if [ "$PR_STATE" = "MERGED" ]; then
    echo "マージ済みブランチを削除: $branch"
    git push origin --delete "$branch"
  fi
done
```

### 2. PRが存在しない孤立ブランチの整理

**これがこのタスクの主要な目的です**

```bash
# すべてのリモートブランチを取得
git fetch --all --prune

# 各ブランチについてPRが存在するかチェック
gh api repos/:owner/:repo/branches --jq '.[] | select(.protected == false) | .name' | while read branch; do
  # main/master/developは除外
  if [[ "$branch" == "main" || "$branch" == "master" || "$branch" == "develop" ]]; then
    continue
  fi

  # このブランチに対応するPRが存在するか確認（Open, Draft, Closed, Mergedすべて）
  PR_COUNT=$(gh pr list --head "$branch" --state all --json number | jq 'length')

  if [ "$PR_COUNT" -eq 0 ]; then
    echo "========================================="
    echo "PRが存在しないブランチ: $branch"

    # ブランチの最終更新日を取得
    LAST_COMMIT_DATE=$(gh api repos/:owner/:repo/branches/$branch --jq '.commit.commit.author.date')
    LAST_COMMIT_SHA=$(gh api repos/:owner/:repo/branches/$branch --jq '.commit.sha')

    # developとの比較（コミット数）
    AHEAD_COUNT=$(git rev-list --count origin/develop..origin/$branch 2>/dev/null || echo "0")

    # ブランチの年齢を計算（日数）
    COMMIT_TIMESTAMP=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$LAST_COMMIT_DATE" +%s 2>/dev/null || echo "0")
    NOW=$(date +%s)
    DAYS_OLD=$(( ($NOW - $COMMIT_TIMESTAMP) / 86400 ))

    echo "最終更新: $LAST_COMMIT_DATE ($DAYS_OLD 日前)"
    echo "developとの差分: +$AHEAD_COUNT コミット"

    # 判断基準
    if [ "$DAYS_OLD" -gt 30 ] && [ "$AHEAD_COUNT" -le 2 ]; then
      # 30日以上古く、コミット数が少ない → 削除
      echo "→ アクション: 削除（古くてコミットが少ない）"
      git push origin --delete "$branch"
      echo "✓ 削除完了: $branch"

    elif [ "$DAYS_OLD" -le 7 ] && [ "$AHEAD_COUNT" -gt 0 ]; then
      # 7日以内で、コミットがある → Draft PR作成
      echo "→ アクション: Draft PR作成（新しくて実装がある）"

      # ブランチの最初のコミットメッセージを取得
      FIRST_COMMIT_MSG=$(git log origin/develop..origin/$branch --oneline --reverse | head -n 1 | cut -d' ' -f2-)

      # Draft PR作成
      gh pr create \
        --head "$branch" \
        --base develop \
        --draft \
        --title "WIP: $FIRST_COMMIT_MSG" \
        --body "## 概要

このPRは孤立していたブランチ \`$branch\` から自動的に作成されました。

## ブランチ情報

- 最終更新: $LAST_COMMIT_DATE
- コミット数: $AHEAD_COUNT
- ブランチ年齢: $DAYS_OLD 日

## 次のステップ

- [ ] このPRの目的を確認
- [ ] 必要な実装を完了
- [ ] テストを追加
- [ ] Ready for Reviewにする

または、不要な場合はPRをクローズしてブランチを削除してください。"

      echo "✓ Draft PR作成完了: $branch"

    elif [ "$AHEAD_COUNT" -gt 5 ]; then
      # コミット数が多い → Issue作成して手動確認
      echo "→ アクション: Issue作成（多くのコミットがあり手動確認が必要）"

      gh issue create \
        --title "確認: ブランチ \`$branch\` の扱いを決定してください" \
        --body "## 概要

ブランチ \`$branch\` にはPRが作成されていませんが、多くの変更があります。

## ブランチ情報

- 最終更新: $LAST_COMMIT_DATE
- ブランチ年齢: $DAYS_OLD 日
- developとの差分: +$AHEAD_COUNT コミット

## コミット履歴

\`\`\`
$(git log origin/develop..origin/$branch --oneline | head -n 10)
\`\`\`

## アクション選択

以下のいずれかを実行してください：

1. **Draft PR作成**: 実装を継続する場合
   \`\`\`bash
   gh pr create --head $branch --base develop --draft --title \"WIP: {タイトル}\"
   \`\`\`

2. **ブランチ削除**: 不要な場合
   \`\`\`bash
   git push origin --delete $branch
   \`\`\`

3. **Issue作成**: 別のIssueとして管理する場合" \
        --label "question,priority:medium"

      echo "✓ Issue作成完了: $branch"

    elif [ "$DAYS_OLD" -gt 14 ]; then
      # 14日以上古い → 削除
      echo "→ アクション: 削除（14日以上更新なし）"
      git push origin --delete "$branch"
      echo "✓ 削除完了: $branch"

    else
      echo "→ アクション: スキップ（判断保留）"
    fi

    echo "========================================="
  fi
done
```

### 3. 削除結果のサマリー

実行後、以下を確認してください：

```bash
# 残っているブランチの一覧
echo "=== 残存ブランチ ==="
gh api repos/:owner/:repo/branches --jq '.[] | select(.protected == false) | .name'

# 新しく作成されたDraft PRの一覧
echo "=== 新規Draft PR ==="
gh pr list --state open --draft --json number,title,headRefName

# 作成された確認Issueの一覧
echo "=== 確認Issue ==="
gh issue list --label "question" --json number,title
```

---

## 📝 完了報告

以下の形式で報告してください：

### 整理したブランチ

- マージ済みブランチを削除: {数}件
- PRなし孤立ブランチを削除: {数}件
- 孤立ブランチからDraft PR作成: {数}件
- 確認Issueを作成: {数}件
- スキップ（判断保留）: {数}件

---

## 🎯 完了基準

- [ ] マージ済みブランチを削除
- [ ] PRが存在しない孤立ブランチを整理（削除/Draft PR作成/Issue作成）
- [ ] 整理結果を報告

**完了したら、このIssueをクローズしてください。**

---

## ⚠️ 重要

- **判断基準に従って自動実行してください**：
  - 30日以上 & コミット少ない（≤2） → 削除
  - 7日以内 & コミットある（>0） → Draft PR作成
  - コミット多い（>5） → Issue作成
  - 14日以上 → 削除
- **Draft PR作成時は明確な説明を含めてください**
- **main/master/developブランチは絶対に削除しないでください**
