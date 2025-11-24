## 🤖 自動プロジェクト管理タスク

このIssueでは、プロジェクト全体の状況を分析し、次に取るべきアクションを決定してください。

### 📊 実行すべき分析

#### 1. 既存PRのレビュー確認
- [ ] `gh pr list --state open` でオープンなPRを確認
- [ ] レビューが必要なPRを特定
- [ ] 優先度の高いPRをレビュー実行

**確認コマンド:**
```bash
gh pr list --state open
gh pr view <PR番号> --comments
```

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

#### 5. 次のアクション決定

以下の優先順位で判断：

1. **Critical**: バグ修正、ブロッカー解消
2. **High**: レビュー待ちPRの処理
3. **Medium**: マイルストーン0の完了
4. **Medium**: マイルストーン1の進行
5. **Low**: ドキュメント改善、最適化

**実行可能なアクション:**
- 最優先Issueを実装する（新しいPR作成）
- PRをレビューする（コメント投稿、Approve/Request Changes）
- 新しいIssueを作成する（バグ、新機能、改善）
- ドキュメントを更新する
- プロジェクト構造を改善する

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
```

#### 検出した問題・課題
```
- 問題の説明
- 影響範囲
- 推奨される対応
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
- 実行時間: X分
```

---

### 🔗 参考リンク

- [プロジェクトボード](https://github.com/users/kkm-horikawa/projects/4)
- [マイルストーン一覧](https://github.com/kkm-horikawa/modern-board/milestones)
- [タスクファイル](../../../docs/tasks/)
- [Issue一覧](https://github.com/kkm-horikawa/modern-board/issues)
- [PR一覧](https://github.com/kkm-horikawa/modern-board/pulls)

---

### 🎯 完了基準

このIssueは以下の条件を満たしたときに完了：

- [ ] 全ての分析項目を実行した
- [ ] 少なくとも1つのアクションを実行した（PR作成/レビュー/Issue作成等）
- [ ] プロジェクト状況サマリーを記載した
- [ ] 実行したアクションを記載した
- [ ] 次回の推奨アクションを記載した

**完了後は自動的にこのIssueをクローズしてください。**
