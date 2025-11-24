"""モデルのユニットテスト.

各モデルの基本的な機能をテストする。
"""

import uuid

import pytest
from django.db.utils import IntegrityError

from api.models import Category, Post, Reaction, Tag, Thread, UserSession


@pytest.mark.django_db
class TestCategoryModel:
    """Categoryモデルのテスト."""

    def test_create_category_success(self):
        """【正常系】カテゴリの作成が正しく動作する.

        【テストの意図】
        カテゴリが正しいデフォルト値で作成されることを保証します。

        【何を保証するか】
        - 必須フィールド（name, slug）でカテゴリを作成できること
        - display_orderのデフォルト値が0であること
        - __str__メソッドがnameを返すこと

        【テスト手順】
        1. 必須フィールドを指定してカテゴリを作成
        2. 各フィールドの値が正しく保存されていることを確認
        3. デフォルト値が正しく設定されていることを確認

        【期待する結果】
        カテゴリが正常に作成され、全てのフィールドが期待通りの値を持つ
        """
        # Arrange & Act
        category = Category.objects.create(
            name="プログラミング",
            slug="programming",
            description="プログラミング関連のスレッド",
        )

        # Assert
        assert category.name == "プログラミング"
        assert category.slug == "programming"
        assert category.display_order == 0
        assert str(category) == "プログラミング"

    def test_category_unique_name(self):
        """【異常系】同じ名前のカテゴリは作成できない.

        【テストの意図】
        カテゴリ名のユニーク制約が正しく機能することを保証します。

        【何を保証するか】
        - 同じnameを持つカテゴリを2つ作成しようとするとIntegrityErrorが発生すること
        - データベースレベルでユニーク制約が機能していること

        【テスト手順】
        1. 特定の名前でカテゴリを作成
        2. 同じ名前で別のカテゴリを作成しようとする
        3. IntegrityErrorが発生することを確認

        【期待する結果】
        IntegrityErrorが発生し、重複したカテゴリは作成されない
        """
        # Arrange
        Category.objects.create(name="雑談", slug="chat")

        # Act & Assert
        with pytest.raises(IntegrityError):
            Category.objects.create(name="雑談", slug="chat2")

    def test_category_ordering(self):
        """【動作確認】カテゴリが表示順序でソートされる.

        【テストの意図】
        Meta.orderingの設定が正しく動作することを保証します。

        【何を保証するか】
        - QuerySetがdisplay_order昇順、name昇順でソートされること
        - 複数のカテゴリを作成した際に期待通りの順序で取得できること

        【テスト手順】
        1. 異なるdisplay_orderを持つ3つのカテゴリを作成
        2. Category.objects.all()でカテゴリを取得
        3. 取得順序がdisplay_order昇順であることを確認

        【期待する結果】
        カテゴリがdisplay_order昇順でソートされて取得される
        """
        # Arrange
        cat1 = Category.objects.create(name="カテゴリ1", slug="cat1", display_order=3)
        cat2 = Category.objects.create(name="カテゴリ2", slug="cat2", display_order=1)
        cat3 = Category.objects.create(name="カテゴリ3", slug="cat3", display_order=2)

        # Act
        categories = list(Category.objects.all())

        # Assert
        assert categories[0] == cat2  # display_order=1
        assert categories[1] == cat3  # display_order=2
        assert categories[2] == cat1  # display_order=3


@pytest.mark.django_db
class TestTagModel:
    """Tagモデルのテスト."""

    def test_create_tag_success(self):
        """【正常系】タグの作成が正しく動作する.

        【テストの意図】
        タグが正しく作成されることを保証します。

        【何を保証するか】
        - 必須フィールド（name, slug）でタグを作成できること
        - __str__メソッドがnameを返すこと

        【テスト手順】
        1. 必須フィールドを指定してタグを作成
        2. 各フィールドの値が正しく保存されていることを確認

        【期待する結果】
        タグが正常に作成され、全てのフィールドが期待通りの値を持つ
        """
        # Arrange & Act
        tag = Tag.objects.create(name="Python", slug="python")

        # Assert
        assert tag.name == "Python"
        assert tag.slug == "python"
        assert str(tag) == "Python"

    def test_tag_unique_name(self):
        """【異常系】同じ名前のタグは作成できない.

        【テストの意図】
        タグ名のユニーク制約が正しく機能することを保証します。

        【何を保証するか】
        - 同じnameを持つタグを2つ作成しようとするとIntegrityErrorが発生すること

        【テスト手順】
        1. 特定の名前でタグを作成
        2. 同じ名前で別のタグを作成しようとする
        3. IntegrityErrorが発生することを確認

        【期待する結果】
        IntegrityErrorが発生し、重複したタグは作成されない
        """
        # Arrange
        Tag.objects.create(name="React", slug="react")

        # Act & Assert
        with pytest.raises(IntegrityError):
            Tag.objects.create(name="React", slug="react2")


@pytest.mark.django_db
class TestUserSessionModel:
    """UserSessionモデルのテスト."""

    def test_create_user_session_success(self):
        """【正常系】ユーザーセッションの作成が正しく動作する.

        【テストの意図】
        ユーザーセッションが正しいデフォルト値で作成されることを保証します。

        【何を保証するか】
        - 必須フィールド（temporary_name）でセッションを作成できること
        - session_idが自動的にUUIDとして生成されること
        - 数値フィールドのデフォルト値が正しく設定されること

        【テスト手順】
        1. temporary_nameを指定してセッションを作成
        2. 各フィールドの値が正しく保存されていることを確認
        3. デフォルト値が正しく設定されていることを確認

        【期待する結果】
        セッションが正常に作成され、全てのフィールドが期待通りの値を持つ
        """
        # Arrange & Act
        session = UserSession.objects.create(temporary_name="ID:abc123")

        # Assert
        assert session.temporary_name == "ID:abc123"
        assert session.post_count == 0
        assert session.thread_count == 0
        assert session.total_points == 0
        assert session.level == 1
        assert isinstance(session.session_id, uuid.UUID)

    def test_user_session_auto_uuid(self):
        """【動作確認】セッションIDが自動生成される.

        【テストの意図】
        session_idが自動的にユニークなUUIDとして生成されることを保証します。

        【何を保証するか】
        - 複数のセッションを作成した際に、それぞれ異なるUUIDが生成されること
        - UUIDの型がuuid.UUIDであること

        【テスト手順】
        1. 2つのセッションを作成
        2. それぞれのsession_idが異なることを確認
        3. UUIDの型を確認

        【期待する結果】
        各セッションがユニークなUUIDを持つ
        """
        # Arrange & Act
        session1 = UserSession.objects.create(temporary_name="ID:user1")
        session2 = UserSession.objects.create(temporary_name="ID:user2")

        # Assert
        assert session1.session_id != session2.session_id
        assert isinstance(session1.session_id, uuid.UUID)
        assert isinstance(session2.session_id, uuid.UUID)

    def test_user_session_unique_session_id(self):
        """【異常系】同じセッションIDは作成できない.

        【テストの意図】
        session_idのユニーク制約が正しく機能することを保証します。

        【何を保証するか】
        - 同じsession_idを持つセッションを2つ作成しようとすると
          IntegrityErrorが発生すること

        【テスト手順】
        1. 特定のUUIDでセッションを作成
        2. 同じUUIDで別のセッションを作成しようとする
        3. IntegrityErrorが発生することを確認

        【期待する結果】
        IntegrityErrorが発生し、重複したセッションは作成されない
        """
        # Arrange
        session_id = uuid.uuid4()
        UserSession.objects.create(temporary_name="ID:user1", session_id=session_id)

        # Act & Assert
        with pytest.raises(IntegrityError):
            UserSession.objects.create(temporary_name="ID:user2", session_id=session_id)


@pytest.mark.django_db
class TestThreadModel:
    """Threadモデルのテスト."""

    def test_create_thread_success(self):
        """【正常系】スレッドの作成が正しく動作する.

        【テストの意図】
        スレッドが正しいデフォルト値で作成されることを保証します。

        【何を保証するか】
        - 必須フィールド（title, category）でスレッドを作成できること
        - 数値フィールドのデフォルト値が正しく設定されること
        - ブールフィールドのデフォルト値が正しく設定されること

        【テスト手順】
        1. カテゴリを作成
        2. 必須フィールドを指定してスレッドを作成
        3. 各フィールドの値が正しく保存されていることを確認

        【期待する結果】
        スレッドが正常に作成され、全てのフィールドが期待通りの値を持つ
        """
        # Arrange
        category = Category.objects.create(name="雑談", slug="chat")

        # Act
        thread = Thread.objects.create(title="テストスレッド", category=category)

        # Assert
        assert thread.title == "テストスレッド"
        assert thread.category == category
        assert thread.post_count == 0
        assert thread.view_count == 0
        assert thread.momentum == 0.0
        assert not thread.is_pinned
        assert not thread.is_locked
        assert str(thread) == "テストスレッド"

    def test_thread_with_tags(self):
        """【動作確認】スレッドにタグを関連付けられる.

        【テストの意図】
        ManyToManyFieldによるタグの関連付けが正しく動作することを保証します。

        【何を保証するか】
        - スレッドに複数のタグを関連付けられること
        - 関連付けたタグがQuerySetで取得できること

        【テスト手順】
        1. カテゴリとタグを作成
        2. スレッドを作成してタグを関連付け
        3. 関連付けたタグが正しく取得できることを確認

        【期待する結果】
        スレッドに複数のタグが正しく関連付けられる
        """
        # Arrange
        category = Category.objects.create(name="プログラミング", slug="programming")
        tag1 = Tag.objects.create(name="Python", slug="python")
        tag2 = Tag.objects.create(name="Django", slug="django")
        thread = Thread.objects.create(title="Djangoチュートリアル", category=category)

        # Act
        thread.tags.add(tag1, tag2)

        # Assert
        assert thread.tags.count() == 2
        assert tag1 in thread.tags.all()
        assert tag2 in thread.tags.all()

    def test_thread_ordering(self):
        """【動作確認】スレッドがピン留め・最終投稿日時でソートされる.

        【テストの意図】
        Meta.orderingの設定が正しく動作することを保証します。

        【何を保証するか】
        - QuerySetがis_pinned降順（Trueが先）でソートされること
        - ピン留めスレッドが通常スレッドより前に表示されること

        【テスト手順】
        1. ピン留めスレッドと通常スレッドを作成
        2. Thread.objects.all()でスレッドを取得
        3. 取得順序がピン留め優先であることを確認

        【期待する結果】
        ピン留めスレッドが先頭に表示される
        """
        # Arrange
        category = Category.objects.create(name="雑談", slug="chat")
        thread1 = Thread.objects.create(
            title="通常スレッド", category=category, is_pinned=False
        )
        thread2 = Thread.objects.create(
            title="ピン留めスレッド", category=category, is_pinned=True
        )

        # Act
        threads = list(Thread.objects.all())

        # Assert - ピン留めが優先
        assert threads[0] == thread2
        assert threads[1] == thread1


@pytest.mark.django_db
class TestPostModel:
    """Postモデルのテスト."""

    def test_create_post_success(self):
        """【正常系】レスの作成が正しく動作する.

        【テストの意図】
        レスが正しく作成されることを保証します。

        【何を保証するか】
        - 必須フィールド（thread, content, post_number）でレスを作成できること
        - is_opフラグが正しく設定されること
        - __str__メソッドが適切な文字列を返すこと

        【テスト手順】
        1. カテゴリとスレッドを作成
        2. 必須フィールドを指定してレスを作成
        3. 各フィールドの値が正しく保存されていることを確認

        【期待する結果】
        レスが正常に作成され、全てのフィールドが期待通りの値を持つ
        """
        # Arrange
        category = Category.objects.create(name="雑談", slug="chat")
        thread = Thread.objects.create(title="テストスレッド", category=category)

        # Act
        post = Post.objects.create(
            thread=thread, content="テスト投稿", post_number=1, is_op=True
        )

        # Assert
        assert post.thread == thread
        assert post.content == "テスト投稿"
        assert post.post_number == 1
        assert post.is_op
        assert "Post #1" in str(post)

    def test_post_unique_together_thread_and_number(self):
        """【異常系】同じスレッド内で同じレス番号は作成できない.

        【テストの意図】
        unique_together制約が正しく機能することを保証します。

        【何を保証するか】
        - 同じスレッド内で同じpost_numberを持つレスを2つ作成できないこと
        - データベースレベルでユニーク制約が機能していること

        【テスト手順】
        1. スレッドを作成
        2. post_number=1でレスを作成
        3. 同じスレッド・同じpost_numberでレスを作成しようとする
        4. IntegrityErrorが発生することを確認

        【期待する結果】
        IntegrityErrorが発生し、重複したレスは作成されない
        """
        # Arrange
        category = Category.objects.create(name="雑談", slug="chat")
        thread = Thread.objects.create(title="テストスレッド", category=category)
        Post.objects.create(thread=thread, content="投稿1", post_number=1)

        # Act & Assert
        with pytest.raises(IntegrityError):
            Post.objects.create(thread=thread, content="投稿2", post_number=1)

    def test_post_with_reply_to(self):
        """【動作確認】レスに返信元を設定できる.

        【テストの意図】
        ForeignKey（self参照）による返信機能が正しく動作することを保証します。

        【何を保証するか】
        - レスに返信元レスを設定できること
        - 返信元レスから返信レスを逆参照できること

        【テスト手順】
        1. スレッドを作成
        2. 元投稿レスを作成
        3. 返信レスを作成してreply_toを設定
        4. 関連が正しく設定されていることを確認

        【期待する結果】
        返信機能が正しく動作し、双方向の参照が可能
        """
        # Arrange
        category = Category.objects.create(name="雑談", slug="chat")
        thread = Thread.objects.create(title="テストスレッド", category=category)
        post1 = Post.objects.create(
            thread=thread, content="元投稿", post_number=1, is_op=True
        )

        # Act
        post2 = Post.objects.create(
            thread=thread, content="返信", post_number=2, reply_to=post1
        )

        # Assert
        assert post2.reply_to == post1
        assert post1.replies.count() == 1
        assert post1.replies.first() == post2


@pytest.mark.django_db
class TestReactionModel:
    """Reactionモデルのテスト."""

    def test_create_reaction_success(self):
        """【正常系】リアクションの作成が正しく動作する.

        【テストの意図】
        リアクションが正しく作成されることを保証します。

        【何を保証するか】
        - 必須フィールド（post, reaction_type）でリアクションを作成できること
        - user_sessionとの関連が正しく設定されること
        - __str__メソッドが適切な文字列を返すこと

        【テスト手順】
        1. カテゴリ、スレッド、レス、セッションを作成
        2. 必須フィールドを指定してリアクションを作成
        3. 各フィールドの値が正しく保存されていることを確認

        【期待する結果】
        リアクションが正常に作成され、全てのフィールドが期待通りの値を持つ
        """
        # Arrange
        category = Category.objects.create(name="雑談", slug="chat")
        thread = Thread.objects.create(title="テストスレッド", category=category)
        post = Post.objects.create(thread=thread, content="投稿", post_number=1)
        session = UserSession.objects.create(temporary_name="ID:user1")

        # Act
        reaction = Reaction.objects.create(
            post=post, user_session=session, reaction_type="like"
        )

        # Assert
        assert reaction.post == post
        assert reaction.user_session == session
        assert reaction.reaction_type == "like"
        assert "like" in str(reaction)

    def test_reaction_unique_together(self):
        """【異常系】同じセッションから同じレスへの同じリアクションは1回のみ.

        【テストの意図】
        unique_together制約が正しく機能することを保証します。

        【何を保証するか】
        - 同じpost、user_session、reaction_typeの組み合わせで
          リアクションを2つ作成できないこと
        - 重複リアクションが防止されること

        【テスト手順】
        1. レスとセッションを作成
        2. 特定のリアクションを作成
        3. 同じレス・同じセッション・同じリアクションタイプで再度作成を試みる
        4. IntegrityErrorが発生することを確認

        【期待する結果】
        IntegrityErrorが発生し、重複したリアクションは作成されない
        """
        # Arrange
        category = Category.objects.create(name="雑談", slug="chat")
        thread = Thread.objects.create(title="テストスレッド", category=category)
        post = Post.objects.create(thread=thread, content="投稿", post_number=1)
        session = UserSession.objects.create(temporary_name="ID:user1")
        Reaction.objects.create(post=post, user_session=session, reaction_type="like")

        # Act & Assert - 重複リアクションはエラー
        with pytest.raises(IntegrityError):
            Reaction.objects.create(
                post=post, user_session=session, reaction_type="like"
            )

    def test_different_reaction_types_allowed(self):
        """【動作確認】同じセッションから異なるリアクションタイプは許可される.

        【テストの意図】
        同一セッションから異なるリアクションタイプは作成可能であることを保証します。

        【何を保証するか】
        - 同じセッション・同じレスでも、異なるreaction_typeであれば複数作成できること
        - unique_together制約がreaction_typeも含めて評価されていること

        【テスト手順】
        1. レスとセッションを作成
        2. "like"リアクションを作成
        3. 同じセッション・同じレスで"funny"リアクションを作成
        4. 両方のリアクションが正常に作成されることを確認

        【期待する結果】
        異なるリアクションタイプであれば複数作成可能
        """
        # Arrange
        category = Category.objects.create(name="雑談", slug="chat")
        thread = Thread.objects.create(title="テストスレッド", category=category)
        post = Post.objects.create(thread=thread, content="投稿", post_number=1)
        session = UserSession.objects.create(temporary_name="ID:user1")

        # Act
        reaction1 = Reaction.objects.create(
            post=post, user_session=session, reaction_type="like"
        )
        reaction2 = Reaction.objects.create(
            post=post, user_session=session, reaction_type="funny"
        )

        # Assert
        assert reaction1.reaction_type == "like"
        assert reaction2.reaction_type == "funny"
        assert post.reactions.count() == 2
