## 📦 Issue分解タスク

**今すぐ実行：**
1. `atomic`も`parent`もないIssueを1つ選ぶ
2. 分解が必要か判断（1クラス/1メソッド粒度か？）
3. 必要なら子Issueを作成（マイルストーン・プロジェクト・ブランチ・PR自動設定）
4. 子Issueに@Claudeメンションして再帰的分解
5. 不要なら`atomic`ラベルを付けて終了

**禁止：**
- ❌ 分析だけで終わる
- ❌ 複数のIssueに手を出す

---

## 実行

```bash
# 1. 対象Issue選択（atomicもparentもないもの）
TARGET=$(gh issue list --state open --json number,labels \
  --jq '.[] | select(.labels | map(.name) | contains(["atomic","parent"]) | not) | .number' \
  | head -1)

gh issue view $TARGET

# 判断A: 分解不要 → atomicラベル
gh issue edit $TARGET --add-label "atomic"
gh issue close {THIS_ISSUE} --comment "完了"

# 判断B: 分解必要 → 以下実行

# 2. 親にparentラベル + ブランチ戦略コメント
gh issue edit $TARGET --add-label "parent"
gh issue comment $TARGET --body "## ブランチ戦略
**親ブランチ**: \`claude/parent-issue-${TARGET}-$(date +%Y%m%d-%H%M)\`
**子PR先**: 親ブランチ → **親PR先**: develop"

# 3. 子Issue作成（スクリプト使用で自動設定）
# マイルストーン・プロジェクト・ブランチ・Draft PR・Development紐付けを自動化
CHILD1=$(.github/scripts/create-child-issue.sh $TARGET \
  "子: {具体的クラス/メソッド名1}" \
  "親Issue: #${TARGET}

## 要件
- {1つの明確な要件}

## 実装
- {1クラス/1メソッド}

## テスト
- [ ] {1テストケース}")

CHILD2=$(.github/scripts/create-child-issue.sh $TARGET \
  "子: {具体的クラス/メソッド名2}" \
  "親Issue: #${TARGET}

## 要件
- {1つの明確な要件}

## 実装
- {1クラス/1メソッド}

## テスト
- [ ] {1テストケース}")

# 4. 親Issueに子リスト追加
gh issue comment $TARGET --body "## 子Issue
- [ ] #${CHILD1}
- [ ] #${CHILD2}

全完了後に\`atomic\`ラベル付与"

# 5. 子に@Claudeメンションして再帰分解
gh issue comment $CHILD1 --body "@claude 1クラス/1メソッド粒度？(A)適切→atomicラベル (B)粗い→子Issue作成。必ず実行。"
gh issue comment $CHILD2 --body "@claude 1クラス/1メソッド粒度？(A)適切→atomicラベル (B)粗い→子Issue作成。必ず実行。"

# 6. 完了
gh issue close {THIS_ISSUE} --comment "完了"
```

**粒度基準**: 1クラス/1メソッド。実装+テスト1項目+要件1つ。
**自動設定**: マイルストーン・プロジェクト・ブランチ・Draft PR・Development紐付け。
