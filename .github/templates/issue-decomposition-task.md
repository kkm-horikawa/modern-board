## 📦 Issue分解タスク

**今すぐ実行：**
1. `atomic`も`parent`もないIssueを1つ選ぶ
2. 分解が必要か判断（1クラス/1メソッド粒度か？）
3. 必要なら子Issueを作成（マイルストーン・プロジェクト・ブランチ・PR自動設定）
4. 子Issueに@Claudeメンションして再帰的分解
5. 不要なら`atomic`ラベルを付けて終了

**禁止：**
- ❌ 分析・推奨・説明だけで終わる
- ❌ 「〇〇すべき」「推奨します」で終わる
- ❌ コマンド実行しない
- ❌ 複数のIssueに手を出す

---

## 実行

```bash
# 1. 対象Issue選択（atomicもparentもない、マイルストーン番号が最小のもの）
TARGET=$(gh issue list --state open --limit 100 --json number,labels,milestone \
  --jq 'map(select(.labels | map(.name) | contains(["atomic","parent"]) | not))
        | sort_by(.milestone.number // 999)
        | .[0].number')

gh issue view $TARGET

# 判断A: 分解不要 → atomicラベル
gh issue edit $TARGET --add-label "atomic"
gh issue close {THIS_ISSUE} --comment "完了"

# 判断B: 分解必要 → 以下実行

# 2. 親Issueの設定確認・補完
# マイルストーン未設定なら最新openマイルストーンを設定
MILESTONE=$(gh issue view $TARGET --json milestone --jq '.milestone.title')
if [ -z "$MILESTONE" ] || [ "$MILESTONE" = "null" ]; then
  DEFAULT_MILESTONE=$(gh api repos/{owner}/{repo}/milestones --jq '[.[] | select(.state=="open")] | .[0].title')
  gh issue edit $TARGET --milestone "$DEFAULT_MILESTONE"
fi

# プロジェクト未設定ならメインプロジェクトに追加
PROJECT=$(gh issue view $TARGET --json projectItems --jq '.projectItems[0].project.title')
if [ -z "$PROJECT" ] || [ "$PROJECT" = "null" ]; then
  gh issue edit $TARGET --add-project "掲示板アプリ開発"
fi

# リレーション・PR確認をClaudeに依頼
gh issue comment $TARGET --body "@claude 未設定なら即実行：1.親Issue参照（本文に親Issue: #N追加）2.Draft PR（なければ作成）禁止：分析だけ。"

# 3. 親にparentラベル + ブランチ戦略コメント
gh issue edit $TARGET --add-label "parent"
gh issue comment $TARGET --body "## ブランチ戦略
**親ブランチ**: \`claude/parent-issue-${TARGET}-$(date +%Y%m%d-%H%M)\`
**子PR先**: 親ブランチ → **親PR先**: develop"

# 4. 子Issue作成（スクリプト使用で自動設定）
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

# 5. 親Issueに子リスト追加
gh issue comment $TARGET --body "## 子Issue
- [ ] #${CHILD1}
- [ ] #${CHILD2}

全完了後に\`atomic\`ラベル付与"

# 6. 子に@Claudeメンションして再帰分解
gh issue comment $CHILD1 --body "@claude 判断後に即実行：(A)粒度OK→\`gh issue edit {N} --add-label atomic\`実行 (B)粗い→子Issue作成実行。禁止：分析だけ、推奨だけ、説明だけ。コマンド実行のみ。"
gh issue comment $CHILD2 --body "@claude 判断後に即実行：(A)粒度OK→\`gh issue edit {N} --add-label atomic\`実行 (B)粗い→子Issue作成実行。禁止：分析だけ、推奨だけ、説明だけ。コマンド実行のみ。"

# 7. 完了
gh issue close {THIS_ISSUE} --comment "完了"
```

**粒度基準**: 1クラス/1メソッド。実装+テスト1項目+要件1つ。
**自動設定**: マイルストーン・プロジェクト・ブランチ・Draft PR・Development紐付け。
