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
        """正常系: カテゴリが正しく作成される."""
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
        """異常系: 同じ名前のカテゴリは作成できない."""
        # Arrange
        Category.objects.create(name="雑談", slug="chat")

        # Act & Assert
        with pytest.raises(IntegrityError):
            Category.objects.create(name="雑談", slug="chat2")

    def test_category_ordering(self):
        """カテゴリが表示順序でソートされる."""
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
        """正常系: タグが正しく作成される."""
        # Arrange & Act
        tag = Tag.objects.create(name="Python", slug="python")

        # Assert
        assert tag.name == "Python"
        assert tag.slug == "python"
        assert str(tag) == "Python"

    def test_tag_unique_name(self):
        """異常系: 同じ名前のタグは作成できない."""
        # Arrange
        Tag.objects.create(name="React", slug="react")

        # Act & Assert
        with pytest.raises(IntegrityError):
            Tag.objects.create(name="React", slug="react2")


@pytest.mark.django_db
class TestUserSessionModel:
    """UserSessionモデルのテスト."""

    def test_create_user_session_success(self):
        """正常系: ユーザーセッションが正しく作成される."""
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
        """セッションIDが自動生成される."""
        # Arrange & Act
        session1 = UserSession.objects.create(temporary_name="ID:user1")
        session2 = UserSession.objects.create(temporary_name="ID:user2")

        # Assert
        assert session1.session_id != session2.session_id
        assert isinstance(session1.session_id, uuid.UUID)
        assert isinstance(session2.session_id, uuid.UUID)

    def test_user_session_unique_session_id(self):
        """異常系: 同じセッションIDは作成できない."""
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
        """正常系: スレッドが正しく作成される."""
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
        """スレッドにタグを関連付けられる."""
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
        """スレッドがピン留め・最終投稿日時でソートされる."""
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
        """正常系: レスが正しく作成される."""
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
        """異常系: 同じスレッド内で同じレス番号は作成できない."""
        # Arrange
        category = Category.objects.create(name="雑談", slug="chat")
        thread = Thread.objects.create(title="テストスレッド", category=category)
        Post.objects.create(thread=thread, content="投稿1", post_number=1)

        # Act & Assert
        with pytest.raises(IntegrityError):
            Post.objects.create(thread=thread, content="投稿2", post_number=1)

    def test_post_with_reply_to(self):
        """レスに返信元を設定できる."""
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
        """正常系: リアクションが正しく作成される."""
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
        """異常系: 同じセッションから同じレスへの同じリアクションは1回のみ."""
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
        """同じセッションから異なるリアクションタイプは許可される."""
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
