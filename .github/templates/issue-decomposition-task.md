## 📦 Issue分解タスク

**今すぐ実行：**
1. `atomic`ラベルがないIssueを1つ選ぶ
2. 分解が必要か判断
3. 必要なら子Issueを作成（1クラス/1メソッド粒度）
4. **子Issueに@Claudeメンションして再帰的に分解継続**
5. 不要なら`atomic`ラベルを付けて終了
6. このIssueをクローズする

**重要：再帰的分解**
- 子Issueがまだ`atomic`でない場合、さらに分解が必要
- 子Issue作成後に@Claudeメンションして自動分解を継続
- すべての子Issueが`atomic`になるまで繰り返す

**禁止：**
- ❌ 分析だけで終わる
- ❌ 複数のIssueに手を出す
- ❌ 分解判断を保留する
- ❌ 子Issueをatomicにせず放置する

---

## 実行

```bash
# 1. 対象Issueを選ぶ（atomicラベルがないもの）
gh issue list --state open --json number,title,labels \
  --jq '.[] | select(.labels | map(.name) | contains(["atomic"]) | not) | .number' \
  | head -1

# 2. Issue内容を確認して分解判断
gh issue view {N}

# 判断A: 分解不要（1クラス/1メソッド/定義のみ） → atomicラベルを付ける
gh issue edit {N} --add-label "atomic"
gh issue close {THIS_ISSUE} --comment "完了"

# 判断B: 分解必要 → 以下を実行

# 3. 親Issueにラベルとブランチ戦略を追加
gh issue edit {N} --add-label "parent"
gh issue comment {N} --body "## ブランチ戦略

**親ブランチ**: \`claude/parent-issue-{N}-$(date +%Y%m%d-%H%M)\`
**子Issue PR先**: 親ブランチ
**親Issue PR先**: \`develop\`

全ての子Issueが完了したら親ブランチをdevelopにマージ"

# 4. 子Issueを作成（目標: 実装+テスト1項目+要件1つ）
# 縦方向分解例: 機能を段階に分割
gh issue create \
  --title "子: {具体的なクラス/メソッド名}" \
  --body "親Issue: #{N}

## 要件
- {1つの明確な要件}

## 実装内容
- {1クラスまたは1メソッドの実装}

## テスト
- [ ] {1つの具体的なテストケース}

## ブランチ戦略
\`\`\`bash
git checkout develop && git pull
git checkout -b claude/parent-issue-{N}-$(date +%Y%m%d-%H%M)
git push origin HEAD

# 子Issue用ブランチ（親ブランチから切る）
git checkout claude/parent-issue-{N}-YYYYMMDD-HHMM
git checkout -b claude/child-issue-{M}-$(date +%Y%m%d-%H%M)
# PR先: claude/parent-issue-{N}-YYYYMMDD-HHMM
\`\`\`" \
  --label "child,automation,implementation"

# 横方向分解例: 関連機能を並列展開
# （複数の独立したクラス/モジュールなど、同じパターンで複数作成）

# 5. 親Issueに子Issueリストを追加
gh issue comment {N} --body "## 子Issue

- [ ] #{子Issue番号1}
- [ ] #{子Issue番号2}
- [ ] #{子Issue番号3}

全て完了後に\`atomic\`ラベルを付与"

# 6. 子Issueに@Claudeメンションして再帰的に分解継続
# 子Issueがまだatomicでない場合、さらに分解される
CHILD_ISSUE_1={子Issue番号1}
CHILD_ISSUE_2={子Issue番号2}
CHILD_ISSUE_3={子Issue番号3}

gh issue comment $CHILD_ISSUE_1 --body "@claude このIssueが1クラス/1メソッド粒度か判断し、(A)粒度が適切→atomicラベル付与、(B)まだ粗い→必ず子Issue作成して分解実行。禁止：推奨だけで終わる、分析だけで終わる。必ずatomicラベル付与または子Issue作成を実行してください。"

gh issue comment $CHILD_ISSUE_2 --body "@claude このIssueが1クラス/1メソッド粒度か判断し、(A)粒度が適切→atomicラベル付与、(B)まだ粗い→必ず子Issue作成して分解実行。禁止：推奨だけで終わる、分析だけで終わる。必ずatomicラベル付与または子Issue作成を実行してください。"

gh issue comment $CHILD_ISSUE_3 --body "@claude このIssueが1クラス/1メソッド粒度か判断し、(A)粒度が適切→atomicラベル付与、(B)まだ粗い→必ず子Issue作成して分解実行。禁止：推奨だけで終わる、分析だけで終わる。必ずatomicラベル付与または子Issue作成を実行してください。"

# 7. このIssueをクローズ
gh issue close {THIS_ISSUE} --comment "完了"
```

**粒度基準**: 1クラス/1メソッド/定義のみ。実装+テスト1項目+要件1つが目安。
**ブランチ戦略**: 子Issue → 親ブランチ → develop でコンフリクト防止。
