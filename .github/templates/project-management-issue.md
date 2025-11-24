## 🤖 自動プロジェクト管理タスク

このIssueでは、プロジェクト全体の状況を分析し、次に取るべきアクションを決定して実行してください。

---

## 🔧 Step 0: 初回セットアップチェック（最優先）

**⚠️ 最初に必ず実行**: プロジェクトが初期セットアップ済みかチェックしてください。

### チェック項目

1. **GitHubプロジェクトの存在確認**
```bash
# リポジトリにリンクされたプロジェクトを確認
gh project list --owner @me --format json | jq '.projects[] | select(.title | contains("Modern Board"))'
```

2. **マイルストーンの存在確認**
```bash
# マイルストーン一覧を取得
gh api repos/:owner/:repo/milestones | jq 'length'
```

3. **基本ラベルの存在確認**
```bash
# ラベル一覧を取得（特にpriority:*系）
gh label list | grep "priority:"
```

### 初回セットアップが必要な場合

**判断基準**:
- プロジェクトが存在しない、または
- マイルストーンが5件未満（マイルストーン0-4が揃っていない）、または
- 基本ラベルが不足している

**実行手順**:

#### 1. プロジェクト要件を読み取る
```bash
# Modern Board専用のプロジェクトセットアップファイルを確認
cat .github/templates/project-setup.md
```

#### 2. GitHubプロジェクトを作成（存在しない場合）
```bash
# Modern Boardプロジェクトを作成
gh project create --owner @me --title "Modern Board" --body "掲示板アプリケーション - React + FastAPI + PostgreSQL"

# 作成したプロジェクト番号を取得
PROJECT_NUMBER=$(gh project list --owner @me --format json | jq -r '.projects[] | select(.title == "Modern Board") | .number')

# プロジェクトをリポジトリにリンク
gh project link $PROJECT_NUMBER --owner @me
```

#### 3. マイルストーンを作成（不足している場合）
```bash
# project-setup.mdに記載されたModern Board専用のマイルストーンを作成
gh api repos/:owner/:repo/milestones -f title="マイルストーン0: 自動化基盤構築" -f description="Claude完全自律開発システムの構築と動作確認"

gh api repos/:owner/:repo/milestones -f title="マイルストーン1: MVP - ローカル動作確認" -f description="最小限の機能を持つ掲示板アプリのローカル動作確認"

gh api repos/:owner/:repo/milestones -f title="マイルストーン2: フル機能実装" -f description="掲示板として必要な全機能の実装"

gh api repos/:owner/:repo/milestones -f title="マイルストーン3: デプロイと公開" -f description="プロダクション環境へのデプロイと公開"

gh api repos/:owner/:repo/milestones -f title="マイルストーン4: 運用とメンテナンス" -f description="運用開始後の監視、改善、機能追加"
```

#### 4. 基本ラベルを作成（不足している場合）
```bash
# project-setup.mdに記載された推奨ラベルを作成（既存の場合はスキップされる）
# 優先度ラベル
gh label create "priority:critical" --description "最優先で対応が必要" --color "d73a4a" 2>/dev/null || true
gh label create "priority:high" --description "高優先度" --color "ff9800" 2>/dev/null || true
gh label create "priority:medium" --description "中優先度" --color "ffeb3b" 2>/dev/null || true
gh label create "priority:low" --description "低優先度" --color "4caf50" 2>/dev/null || true

# カテゴリラベル
gh label create "feature" --description "新機能" --color "1e88e5" 2>/dev/null || true
gh label create "enhancement" --description "既存機能の改善" --color "42a5f5" 2>/dev/null || true
gh label create "bug" --description "バグ修正" --color "f44336" 2>/dev/null || true
gh label create "documentation" --description "ドキュメント" --color "9c27b0" 2>/dev/null || true
gh label create "testing" --description "テスト関連" --color "673ab7" 2>/dev/null || true
gh label create "infrastructure" --description "インフラ・CI/CD" --color "607d8b" 2>/dev/null || true
gh label create "design" --description "設計・アーキテクチャ" --color "ff5722" 2>/dev/null || true
gh label create "setup" --description "セットアップ関連" --color "795548" 2>/dev/null || true
gh label create "deployment" --description "デプロイ関連" --color "8bc34a" 2>/dev/null || true
gh label create "database" --description "データベース関連" --color "00bcd4" 2>/dev/null || true
gh label create "security" --description "セキュリティ関連" --color "e91e63" 2>/dev/null || true
gh label create "performance" --description "パフォーマンス関連" --color "3f51b5" 2>/dev/null || true
gh label create "monitoring" --description "監視関連" --color "009688" 2>/dev/null || true
gh label create "frontend" --description "フロントエンド関連" --color "61dafb" 2>/dev/null || true
gh label create "backend" --description "バックエンド関連" --color "009688" 2>/dev/null || true
```

#### 5. 初期Issueを作成（該当マイルストーンにIssueがない場合）
```bash
# project-setup.mdに記載された各マイルストーンの初期Issueを作成
# 既存のIssueを確認してから作成

# マイルストーン番号を取得
MILESTONE_0=$(gh api repos/:owner/:repo/milestones | jq -r '.[] | select(.title | contains("マイルストーン0")) | .number')
MILESTONE_1=$(gh api repos/:owner/:repo/milestones | jq -r '.[] | select(.title | contains("マイルストーン1")) | .number')

# マイルストーン0の初期Issue（まだIssueがない場合のみ）
if [ $(gh issue list --milestone $MILESTONE_0 --json number | jq 'length') -eq 0 ]; then
  gh issue create \
    --title "GitHub Actions ワークフローのセットアップ" \
    --body "claude-project-manager.yml、claude.yml、Slack通知の設定" \
    --label "setup,priority:critical,infrastructure" \
    --milestone $MILESTONE_0

  gh issue create \
    --title "プロジェクト管理テンプレートの作成" \
    --body "project-management-issue.mdなどのテンプレート作成" \
    --label "setup,priority:high,documentation" \
    --milestone $MILESTONE_0
fi

# マイルストーン1の初期Issue（例）
if [ $(gh issue list --milestone $MILESTONE_1 --json number | jq 'length') -eq 0 ]; then
  gh issue create \
    --title "FE-001: フロントエンドプロジェクトのセットアップ" \
    --body "React + TypeScript + Vite のセットアップ、アーキテクチャ設計" \
    --label "setup,priority:high,frontend" \
    --milestone $MILESTONE_1

  # 他のIssueも同様に作成...
fi
```

#### 6. 初期セットアップ完了を報告

このIssueに以下を報告してください：
```
✅ 初期セットアップが完了しました

**作成されたリソース:**
- GitHubプロジェクト: Modern Board (#番号)
- マイルストーン: 5件（マイルストーン0-4）
- ラベル: X件
- 初期Issue: Y件

**次のステップ:**
通常のプロジェクト管理タスクを実行します。
```

---

## 📊 実行すべき分析

**注意**: 初回セットアップが完了している場合のみ、以下の分析を実行してください。

#### 1. 既存PRのレビュー確認（Draft PR含む）
- [ ] `gh pr list --state open` でオープンなPRを確認（**Draft PR含む**）
- [ ] **Draft PRが存在するIssueには新たに着手しない**（重複作業防止）
- [ ] レビューが必要なPRを特定
- [ ] 優先度の高いPRをレビュー実行

**確認コマンド:**
```bash
# 全てのPR（Draft含む）を確認
gh pr list --state open

# Draft PRのみ確認
gh pr list --state open --draft

# PRの詳細確認
gh pr view <PR番号> --comments
```

**重要: Draft PRが存在するIssueは作業中のため、新たに着手しないでください**

#### 2. Issue優先順位分析
- [ ] マイルストーン0-4の進捗確認
- [ ] `label:bug` のIssueを確認
- [ ] `label:blocker` のIssueを確認
- [ ] 依存関係をチェック
- [ ] 各マイルストーンの完了率を計算

**確認コマンド:**
```bash
gh issue list --milestone "マイルストーン0: 自動化基盤構築"
gh issue list --milestone "マイルストーン1: MVP - ローカル動作確認"
gh issue list --milestone "マイルストーン2: フル機能実装"
gh issue list --milestone "マイルストーン3: デプロイと公開"
gh issue list --milestone "マイルストーン4: 運用とメンテナンス"
gh issue list --label bug
gh issue list --label blocker
```

#### 3. プロジェクトの健全性チェック
- [ ] 最新のCI/CDワークフローの結果を確認
- [ ] テストカバレッジを確認（backend/frontend）
- [ ] エラーログを確認
- [ ] ビルド失敗の有無を確認

**確認コマンド:**
```bash
gh run list --limit 10
gh run view <run-id>
```

#### 4. タスク進捗確認
- [ ] `docs/tasks/` 配下のタスクファイルを確認
- [ ] 実装済みタスクと未着手タスクの差分を確認
- [ ] 新規Issueが必要なタスクを特定

#### 5. マイルストーンとプロジェクトボード管理
- [ ] マイルストーンの進捗状況を確認
- [ ] 完了したマイルストーンがあればクローズ
- [ ] 新しいマイルストーンが必要か判断
- [ ] Issueに適切なマイルストーンを割り当て
- [ ] プロジェクトボードにIssue/PRを追加

**管理コマンド:**
```bash
# マイルストーン一覧
gh api repos/:owner/:repo/milestones

# Issueにマイルストーン割り当て
gh issue edit <Issue番号> --milestone "マイルストーン名"

# プロジェクトボードに追加
gh project item-add <プロジェクト番号> --owner @me --url <Issue/PR URL>
```

#### 6. 停滞タスクの検出と再実行

**⚠️ 重要: 以下のケースを検出し、再度実行を促してください**

- [ ] `@claude` メンションがあるのにClaudeが応答していないIssue/PR
- [ ] Draft PRが48時間以上更新されていない
- [ ] レビュー待ちPRが72時間以上放置されている
- [ ] Issueがアサインされているが7日以上更新がない

**検出コマンド:**
```bash
# 最近のIssueコメントをチェック（@claudeメンション検索）
gh issue list --state open --json number,title,comments,updatedAt | \
  jq '.[] | select(.comments[-1].body | contains("@claude"))'

# Draft PRで長期間更新がないものを検出（48時間以上）
gh pr list --state open --draft --json number,title,updatedAt | \
  jq --arg date "$(date -u -v-48H +%Y-%m-%dT%H:%M:%SZ)" \
  '.[] | select(.updatedAt < $date)'

# 特定のIssueの最後のコメントを確認
gh issue view <Issue番号> --json comments | \
  jq '.comments[-1] | {author: .author.login, body: .body, createdAt: .createdAt}'
```

**再実行アクション:**

停滞していると判断したIssue/PRには、再度 `@claude` メンションを投稿してください：

```bash
# 例: Issue #3でClaudeの応答がない場合
gh issue comment 3 --body "@claude 前回のメンションから応答がありません。このタスクの実行を再開してください。"

# 例: Draft PRが停滞している場合
gh pr comment <PR番号> --body "@claude このDraft PRが48時間以上更新されていません。実装を継続するか、ブロッカーがあればコメントしてください。"
```

#### 7. 次のアクション決定と実行

以下の優先順位で判断し、**実際に実行**してください：

1. **Critical**: バグ修正、ブロッカー解消
2. **High**: 停滞タスクの検出と再実行（セクション6参照）
3. **High**: レビュー待ちPRの処理
4. **Medium**: マイルストーン0の完了
5. **Medium**: マイルストーン1の進行
6. **Low**: ドキュメント改善、最適化

**⚠️ 重要: 重複作業の防止**

新しいIssueに着手する前に、必ず以下を確認してください：
```bash
# そのIssueに関連するPR（Draft含む）が既に存在しないか確認
gh pr list --state open --search "in:title Issue番号 OR in:body Closes OR in:body Close"
```

**Draft PRが存在する場合は、そのIssueには着手せず、他の優先度の高いタスクを選択してください。**

**実行可能なアクション:**
- 最優先Issueを実装する（**Draft PRが存在しないことを確認後**）
- PRをレビューする（コメント投稿、Approve/Request Changes）
- 新しいIssueを作成する（バグ、新機能、改善）
- Issueにマイルストーンを割り当てる
- プロジェクトボードを更新する
- ディスカッションに進捗報告を投稿する
- ドキュメントを更新する
- プロジェクト構造を改善する

**重要: 推奨アクションの実行方法**

他のIssueに対して推奨事項や分析コメントを投稿する場合：
1. まず推奨内容をコメントとして投稿
2. **その後、同じIssueに `@claude` をメンションした新しいコメントを投稿して実装を開始**

例:
```bash
# Issue #3に推奨事項を投稿
gh issue comment 3 --body "推奨事項: ..."

# 同じIssueに@claudeメンションして実装開始
gh issue comment 3 --body "@claude このIssueの実装を開始してください。"
```

これにより、推奨したタスクが自動的に実行されます。

**重要: Issue実装時のワークフロー（必須）**

Issueの実装を開始する場合、**必ず以下の順序で作業してください：**

1. **Draft PRを先に作成**
   ```bash
   # ブランチを作成
   git checkout -b feature/issue-XX-description

   # 空コミットを作成
   git commit --allow-empty -m "WIP: Issue #XX の実装開始"

   # プッシュ
   git push origin feature/issue-XX-description

   # Draft PRを作成
   gh pr create --draft \
     --title "WIP: Issue #XX タイトル" \
     --body "Issue #XX の実装を進めています。Closes #XX" \
     --base develop
   ```

2. **実装を進める**
   - コードを書く
   - コミットを追加
   - 必要に応じてプッシュ

3. **実装完了後、Draft を解除**
   ```bash
   gh pr ready
   ```

4. **レビュー依頼**
   - PR にコメントでレビューを依頼

**このワークフローを守ることで：**
- 作業の透明性が確保される
- レビュアーが進捗を確認できる
- 並行作業時の競合を防げる

---

### 📝 実行後の報告

**このセクションに以下を記載してください：**

#### プロジェクト状況サマリー
```
- マイルストーン0: X/Y 完了 (Z%)
- マイルストーン1: X/Y 完了 (Z%)
- マイルストーン2: X/Y 完了 (Z%)
- マイルストーン3: X/Y 完了 (Z%)
- マイルストーン4: X/Y 完了 (Z%)
- オープンなPR: X件
- 未解決のバグ: X件
- ブロッカー: X件
```

#### 実行したアクション
```
1. [アクション種別] Issue/PR番号 - 概要
   - 詳細な説明
   - 結果

例:
1. [PR Review] #25 - FE-001のレビュー
   - コンポーネント構造を確認
   - テストカバレッジが十分
   - Approved

2. [Implementation] #3 - FE-001の実装
   - プロジェクトセットアップ完了
   - PR #26 を作成

3. [Milestone Management] Issue #10, #12, #15
   - マイルストーン1に割り当て
   - 依存関係を整理

4. [Project Board] Issue #20, PR #25
   - プロジェクトボードに追加
   - ステータスを"In Progress"に更新

5. [Discussion] 今週の進捗報告
   - 完了したタスクをディスカッションに投稿
   - 次週の計画を共有
```

#### 検出した問題・課題
```
- 問題の説明
- 影響範囲
- 実施した対応 or 推奨される対応
```

#### 次回の推奨アクション
```
- 次に取り組むべきIssue
- 注意すべき点
- ブロッカーとなりうる要素
```

#### 統計情報
```
- 今回処理したIssue数: X
- 今回レビューしたPR数: X
- 今回作成したIssue数: X
- マイルストーン割り当て数: X
- プロジェクトボード更新数: X
- ディスカッション投稿数: X
- 実行時間: X分
```

---

### 🔗 参考リンク

- [プロジェクトボード](https://github.com/users/kkm-horikawa/projects/4)
- [マイルストーン一覧](https://github.com/kkm-horikawa/modern-board/milestones)
- [ディスカッション](https://github.com/kkm-horikawa/modern-board/discussions)
- [タスクファイル](../../../docs/tasks/)
- [Issue一覧](https://github.com/kkm-horikawa/modern-board/issues)
- [PR一覧](https://github.com/kkm-horikawa/modern-board/pulls)

---

### 🎯 完了基準

このIssueは以下の条件を満たしたときに完了：

- [ ] 全ての分析項目を実行した
- [ ] 少なくとも1つのアクションを実行した（PR作成/レビュー/Issue作成/マイルストーン管理/プロジェクトボード更新/ディスカッション投稿等）
- [ ] プロジェクト状況サマリーを記載した
- [ ] 実行したアクションを記載した
- [ ] 次回の推奨アクションを記載した

**完了後は自動的にこのIssueをクローズしてください。**
