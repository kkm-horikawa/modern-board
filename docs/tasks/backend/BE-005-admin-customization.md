# BE-005: Django管理画面のカスタマイズ

## 概要
Django管理画面をカスタマイズし、カテゴリ、タグ、スレッド、投稿を効率的に管理できるようにする。

## 優先度
**Medium** - 運用に必要だが初期リリースには必須ではない

## 難易度
**Easy**

## 前提条件
- [x] モデルが実装済み
- [x] Django管理画面が有効化されている

## 実装内容

### 1. CategoryAdmin
- [ ] リスト表示のカスタマイズ
  ```python
  list_display = ['name', 'slug', 'description', 'order', 'thread_count', 'created_at']
  ```
- [ ] 検索機能の追加
  ```python
  search_fields = ['name', 'description']
  ```
- [ ] フィルタの追加
  ```python
  list_filter = ['created_at']
  ```
- [ ] 並び順の設定
  ```python
  ordering = ['order', 'name']
  ```
- [ ] 読み取り専用フィールド
  ```python
  readonly_fields = ['created_at', 'updated_at', 'thread_count']
  ```
- [ ] スレッド数の計算メソッド追加

### 2. TagAdmin
- [ ] リスト表示のカスタマイズ
  ```python
  list_display = ['name', 'slug', 'usage_count', 'created_at']
  ```
- [ ] 検索機能
  ```python
  search_fields = ['name']
  ```
- [ ] 使用頻度でのフィルタ
- [ ] 読み取り専用フィールド
  ```python
  readonly_fields = ['created_at', 'updated_at', 'usage_count']
  ```
- [ ] 使用数の計算メソッド追加

### 3. ThreadAdmin
- [ ] リスト表示のカスタマイズ
  ```python
  list_display = [
    'title',
    'category',
    'post_count',
    'view_count',
    'is_pinned',
    'is_locked',
    'created_at'
  ]
  ```
- [ ] 検索機能
  ```python
  search_fields = ['title']
  ```
- [ ] フィルタ
  ```python
  list_filter = ['category', 'is_pinned', 'is_locked', 'created_at']
  ```
- [ ] インラインでタグを編集
- [ ] アクション: 一括ピン留め/解除
- [ ] アクション: 一括ロック/解除
- [ ] 読み取り専用フィールド
  ```python
  readonly_fields = ['created_at', 'updated_at', 'last_post_at', 'view_count']
  ```

### 4. PostAdmin
- [ ] リスト表示のカスタマイズ
  ```python
  list_display = [
    'id',
    'thread',
    'post_number',
    'author_name_truncated',
    'content_truncated',
    'created_at'
  ]
  ```
- [ ] 検索機能
  ```python
  search_fields = ['content', 'thread__title']
  ```
- [ ] フィルタ
  ```python
  list_filter = ['thread', 'is_op', 'created_at']
  ```
- [ ] スレッドごとのフィルタ
- [ ] 読み取り専用フィールド
  ```python
  readonly_fields = ['post_number', 'created_at', 'updated_at']
  ```
- [ ] 内容の省略表示メソッド

### 5. UserSessionAdmin
- [ ] リスト表示のカスタマイズ
  ```python
  list_display = ['session_key_truncated', 'ip_address', 'created_at', 'last_activity']
  ```
- [ ] 検索機能
  ```python
  search_fields = ['session_key', 'ip_address']
  ```
- [ ] フィルタ
  ```python
  list_filter = ['created_at', 'last_activity']
  ```
- [ ] セッションキーの省略表示
- [ ] 最終活動日時の表示
- [ ] アクション: 古いセッションの一括削除

### 6. ReactionAdmin
- [ ] リスト表示のカスタマイズ
  ```python
  list_display = ['post', 'reaction_type', 'user_session_truncated', 'created_at']
  ```
- [ ] フィルタ
  ```python
  list_filter = ['reaction_type', 'created_at']
  ```
- [ ] 統計情報の表示（オプション）

### 7. カスタムアクション
- [ ] スレッドの一括ピン留め
- [ ] スレッドの一括ロック
- [ ] 古い投稿の一括削除（慎重に）
- [ ] 古いセッションの一括削除

### 8. 管理画面の見た目改善
- [ ] カスタムCSS の追加（オプション）
- [ ] リスト表示のページネーション設定
- [ ] 日付フィールドのフォーマット統一

### 9. 権限設定
- [ ] スタッフユーザーの権限設定
- [ ] カスタムパーミッションの追加（必要に応じて）
- [ ] モデルレベルの権限制御

## 受け入れ基準
- [ ] すべてのモデルが管理画面に登録されている
- [ ] リスト表示が見やすく、必要な情報が表示される
- [ ] 検索とフィルタが正常に動作する
- [ ] カスタムアクションが実装されている
- [ ] 読み取り専用フィールドが適切に設定されている
- [ ] パフォーマンスが良好（select_related/prefetch_related使用）
- [ ] スタッフユーザーが管理画面にアクセスできる

## 実装例

### CategoryAdmin
```python
from django.contrib import admin
from django.db.models import Count
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'order', 'thread_count_display', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['order', 'name']
    readonly_fields = ['created_at', 'updated_at', 'thread_count_display']
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(thread_count=Count('threads'))

    @admin.display(description='スレッド数', ordering='thread_count')
    def thread_count_display(self, obj):
        return obj.thread_count if hasattr(obj, 'thread_count') else obj.threads.count()
```

### ThreadAdmin with Custom Actions
```python
from django.contrib import admin
from .models import Thread

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'post_count', 'view_count', 'is_pinned', 'is_locked', 'created_at']
    list_filter = ['category', 'is_pinned', 'is_locked', 'created_at']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at', 'last_post_at', 'view_count']
    actions = ['make_pinned', 'make_unpinned', 'make_locked', 'make_unlocked']

    @admin.action(description='選択したスレッドをピン留めする')
    def make_pinned(self, request, queryset):
        updated = queryset.update(is_pinned=True)
        self.message_user(request, f'{updated}件のスレッドをピン留めしました。')

    @admin.action(description='選択したスレッドのピン留めを解除する')
    def make_unpinned(self, request, queryset):
        updated = queryset.update(is_pinned=False)
        self.message_user(request, f'{updated}件のスレッドのピン留めを解除しました。')

    @admin.action(description='選択したスレッドをロックする')
    def make_locked(self, request, queryset):
        updated = queryset.update(is_locked=True)
        self.message_user(request, f'{updated}件のスレッドをロックしました。')

    @admin.action(description='選択したスレッドのロックを解除する')
    def make_unlocked(self, request, queryset):
        updated = queryset.update(is_locked=False)
        self.message_user(request, f'{updated}件のスレッドのロックを解除しました。')
```

## 関連タスク
- なし（独立したタスク）

## 参考
- Django Admin: https://docs.djangoproject.com/en/5.2/ref/contrib/admin/
- Admin Actions: https://docs.djangoproject.com/en/5.2/ref/contrib/admin/actions/
- Customizing Admin: https://docs.djangoproject.com/en/5.2/intro/tutorial07/
