## 📚 ドキュメント整理タスク

**今すぐ実行：**
1. 親Issue（DOC-ORG）の前回整理結果を確認
2. ルール違反を検出（配置場所、300行超え、TL;DRなし）
3. 重複・古いドキュメントを検出
4. 移動・削除・統合を実行
5. docs/README.md を更新
6. 親Issueに最新構造を記録
7. このIssueをクローズする

**禁止：**
- ❌ 分析だけで終わる
- ❌ 新しいドキュメントを安易に作成
- ❌ 構造記録を忘れる

---

## ドキュメント構造ルール

```
docs/
├── README.md           # ドキュメントインデックス（自動生成）
├── development/        # 開発者向け（環境構築、コーディング規約、アーキテクチャ）
├── features/          # 機能説明（1機能=1ファイル）
├── requirements/      # 要件定義
└── design/            # 機能設計
```

**各ドキュメントのルール：**
- **日本語で記載**（コードサンプル以外）
- **300行以内**（超えたら分割）
- **TL;DR必須**（`## TL;DR`セクション）
- **最終更新日**：`最終更新: YYYY-MM-DD`
- **階層は3層まで**

---

## 実行

```bash
# 1. 親Issueを確認（なければ作成）
PARENT=$(gh issue list --label "parent,documentation-org" --state all --limit 1 --json number -q '.[0].number')

if [ -z "$PARENT" ]; then
  PARENT=$(gh issue create \
    --title "DOC-ORG: ドキュメント整理履歴" \
    --body "このIssueはドキュメント整理の履歴を記録します。クローズしないでください。" \
    --label "parent,documentation-org,automation" \
    --json number -q '.number')
fi

echo "親Issue: #${PARENT}"
gh issue view $PARENT

# 2. ルール違反を検出
echo "## ルール違反検出" > /tmp/violations.txt

# A. 配置場所違反（docs/外にある、README.md等を除く）
find . -name "*.md" ! -path "./docs/*" ! -name "README.md" ! -name "CONTRIBUTING.md" ! -path "./.github/*" ! -path "./node_modules/*" >> /tmp/violations.txt

# B. カテゴリなしでdocs/直下にある
find docs/ -maxdepth 1 -name "*.md" ! -name "README.md" >> /tmp/violations.txt

# C. 300行超え
find docs/ -name "*.md" ! -name "README.md" -exec sh -c 'lines=$(wc -l < "$1"); [ $lines -gt 300 ] && echo "$1 (${lines}行)"' _ {} \; >> /tmp/violations.txt

# D. TL;DRなし
find docs/ -name "*.md" ! -name "README.md" -exec sh -c 'grep -q "## TL;DR\|## 概要" "$1" || echo "$1 (TL;DRなし)"' _ {} \; >> /tmp/violations.txt

# E. 最終更新日なし
find docs/ -name "*.md" ! -name "README.md" -exec sh -c 'grep -q "最終更新:" "$1" || echo "$1 (最終更新日なし)"' _ {} \; >> /tmp/violations.txt

# 3. 重複検出（タイトルが類似）
find docs/ -name "*.md" ! -name "README.md" -exec head -1 {} + | sort | uniq -d > /tmp/duplicates.txt

# 4. 古いドキュメント（90日以上更新なし）
find docs/ -name "*.md" ! -name "README.md" -mtime +90 > /tmp/old-docs.txt

# 5. 違反を修正
# A. 配置場所違反 → docs/配下に移動
# B. 300行超え → 分割を提案（手動判断）
# C. TL;DR/最終更新日なし → 追加

# 例: 配置場所違反の修正
while IFS= read -r file; do
  if [ -f "$file" ]; then
    # ファイル名から適切なカテゴリを判断
    basename=$(basename "$file")
    # 例: setup.md → docs/development/
    # 例: feature-xxx.md → docs/features/

    # 適切なカテゴリに移動
    git mv "$file" "docs/development/$basename" || git mv "$file" "docs/features/$basename"
  fi
done < /tmp/violations.txt

# 6. docs/README.md を更新
cat > docs/README.md <<'EOF'
# ドキュメントインデックス

最終更新: $(date +%Y-%m-%d)

## 開発者向け

EOF

find docs/development/ -name "*.md" -exec echo "- [{}]({})" \; >> docs/README.md

cat >> docs/README.md <<'EOF'

## 機能説明

EOF

find docs/features/ -name "*.md" -exec echo "- [{}]({})" \; >> docs/README.md

cat >> docs/README.md <<'EOF'

## 要件定義・設計

EOF

find docs/requirements/ docs/design/ -name "*.md" -exec echo "- [{}]({})" \; >> docs/README.md

# 7. 変更をコミット
git add docs/
git commit -m "docs: ドキュメント整理（ルール違反修正、重複削除、インデックス更新）" || echo "変更なし"
git push origin develop || git push origin HEAD

# 8. 親Issueに記録
CURRENT_STRUCTURE=$(find docs/ -name "*.md" | sort)
CURRENT_HASH=$(echo "$CURRENT_STRUCTURE" | md5sum | cut -d' ' -f1)

gh issue comment $PARENT --body "## $(date +%Y-%m-%d) 整理結果

**ドキュメント構造ハッシュ**: \`${CURRENT_HASH}\`

**ルール違反**: $(wc -l < /tmp/violations.txt)件
**重複**: $(wc -l < /tmp/duplicates.txt)件
**古いドキュメント**: $(wc -l < /tmp/old-docs.txt)件

<details>
<summary>現在のドキュメント一覧</summary>

\`\`\`
${CURRENT_STRUCTURE}
\`\`\`
</details>"

# 9. このIssueをクローズ
gh issue close {THIS_ISSUE} --comment "完了"
```

**必ずdocs/README.md更新と親Issue記録を実行してください。**
