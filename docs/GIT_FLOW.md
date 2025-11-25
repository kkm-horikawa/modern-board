# Git Flow ルール

## ブランチ戦略

```
develop (開発ブランチ)
  ↓ PR（リリース時のみ）
master (本番ブランチ)
```

## 重要なルール

### ✅ やること

1. **全ての開発は`develop`で行う**
   - 新機能、バグ修正、リファクタリングすべて

2. **リリース時のみ`develop` → `master`へPR**
   - PRタイトル: `Release: v1.2.3`
   - squash mergeまたはmerge commit

3. **機能ブランチは`develop`から切る**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/new-feature
   ```

4. **機能ブランチは`develop`へマージ**
   ```bash
   gh pr create --base develop --head feature/new-feature
   ```

### ❌ やってはいけないこと

1. **`master`から`develop`へのマージは禁止**
   - コンフリクトの原因
   - 履歴が複雑化

2. **`master`へ直接コミット禁止**
   - 必ず`develop`経由

3. **ホットフィックスも`develop`で**
   - `master`へ直接PRしない
   - `develop`で修正 → `develop`から`master`へPR

## ワークフロー例

### 新機能開発

```bash
# 1. developから機能ブランチを切る
git checkout develop
git pull origin develop
git checkout -b feature/awesome-feature

# 2. 実装
git add .
git commit -m "feat: Add awesome feature"
git push origin feature/awesome-feature

# 3. developへPR作成
gh pr create --base develop --title "feat: Add awesome feature"

# 4. マージ後、機能ブランチ削除
gh pr merge --squash --delete-branch
```

### リリース

```bash
# 1. developが安定していることを確認
git checkout develop
git pull origin develop

# 2. masterへPR作成
gh pr create --base master --head develop --title "Release: v1.2.3"

# 3. レビュー＆マージ
gh pr merge --squash

# 4. タグ作成
git checkout master
git pull origin master
git tag v1.2.3
git push origin v1.2.3
```

### ホットフィックス

```bash
# 1. developでバグ修正
git checkout develop
git pull origin develop
git checkout -b hotfix/critical-bug

# 2. 修正
git add .
git commit -m "fix: Critical bug"
git push origin hotfix/critical-bug

# 3. developへPR
gh pr create --base develop --title "fix: Critical bug"
gh pr merge --squash --delete-branch

# 4. 緊急ならすぐにmasterへリリース
gh pr create --base master --head develop --title "Hotfix: v1.2.4"
gh pr merge --squash
```

## コンフリクト回避のポイント

1. **一方向のマージのみ**: `develop` → `master`
2. **頻繁にdevelopをpull**: 常に最新に保つ
3. **小さく頻繁にマージ**: 大きな変更を避ける
4. **機能ブランチは短命に**: 長期ブランチは避ける

## 現在の状態

最終更新: 2025-11-25

- `develop`: 開発中の最新コード
- `master`: 本番環境にデプロイ済みのコード
- **双方向マージは終了**: `master` → `develop`のマージは今後行いません

---

## よくある質問

**Q: masterにバグを見つけたらどうする？**
A: `develop`で修正 → `master`へPR（ホットフィックス手順に従う）

**Q: masterとdevelopがずれたら？**
A: 正常です。`develop`が常に先行しています。リリース時のみ`master`に追いつきます。

**Q: コンフリクトが発生したら？**
A: 通常は発生しません。発生した場合は`develop`優先で解決してください。
