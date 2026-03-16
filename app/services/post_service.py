"""
Post service for optimized post queries and operations.
"""
from sqlalchemy.orm import joinedload
from app import db
from app.models import Post, Reply


class PostService:
    """Service for post-related operations"""

    @staticmethod
    def get_by_id_with_relations(post_id):
        """
        Get a post by ID with all relations eager loaded.

        Args:
            post_id (int): Post ID

        Returns:
            Post: Post object with relations loaded or None
        """
        return Post.query.options(
            joinedload(Post.author),
            joinedload(Post.category)
        ).filter_by(id=post_id).first()

    @staticmethod
    def get_replies_paginated(post_id, page=1, per_page=50):
        """
        Get replies for a post with pagination and eager loading.

        Args:
            post_id (int): Post ID
            page (int): Page number
            per_page (int): Replies per page

        Returns:
            dict: Dictionary with 'replies', 'total', 'page', 'per_page'
        """
        query = Reply.query.filter_by(post_id=post_id).options(
            joinedload(Reply.author)  # Eager load author to avoid N+1
        ).order_by(Reply.created_at.asc())

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * per_page
        replies = query.offset(offset).limit(per_page).all()

        return {
            'replies': replies,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }

    @staticmethod
    def create_post(title, content, author_id, category_id, cover_image=None):
        """
        Create a new post.

        Args:
            title (str): Post title
            content (str): Post content
            author_id (int): Author user ID
            category_id (int): Category ID
            cover_image (str): Cover image filename (optional)

        Returns:
            Post: Created post object

        Raises:
            Exception: If database operation fails
        """
        post = Post(
            title=title,
            content=content,
            author_id=author_id,
            category_id=category_id,
            cover_image=cover_image
        )
        db.session.add(post)
        db.session.flush()  # Get post.id without committing
        return post

    @staticmethod
    def delete_post(post_id):
        """
        Delete a post by ID.

        Args:
            post_id (int): Post ID

        Returns:
            bool: True if deleted, False if not found
        """
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            return True
        return False

    @staticmethod
    def create_reply(content, author_id, post_id):
        """
        Create a reply to a post.

        Args:
            content (str): Reply content
            author_id (int): Author user ID
            post_id (int): Post ID

        Returns:
            Reply: Created reply object

        Raises:
            Exception: If database operation fails
        """
        reply = Reply(
            content=content,
            author_id=author_id,
            post_id=post_id
        )
        db.session.add(reply)
        db.session.flush()
        return reply
