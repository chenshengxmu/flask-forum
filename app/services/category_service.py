"""
Category service for optimized category queries.
Fixes N+1 query problems by using eager loading and aggregations.
"""
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app import db
from app.models import Category, Post


class CategoryService:
    """Service for category-related operations"""

    @staticmethod
    def get_all_with_stats():
        """
        Get all categories with post counts and latest post information.
        Uses a single optimized query instead of N+1 queries.

        Returns:
            list: List of tuples (category, post_count, latest_post)
        """
        # Subquery for post counts
        post_counts = db.session.query(
            Post.category_id,
            func.count(Post.id).label('post_count')
        ).group_by(Post.category_id).subquery()

        # Subquery for latest post per category
        latest_posts_subquery = db.session.query(
            Post.category_id,
            func.max(Post.created_at).label('max_created_at')
        ).group_by(Post.category_id).subquery()

        # Main query with eager loading
        results = db.session.query(
            Category,
            func.coalesce(post_counts.c.post_count, 0).label('post_count')
        ).outerjoin(
            post_counts,
            Category.id == post_counts.c.category_id
        ).order_by(Category.name).all()

        # Get latest posts separately (more efficient than joining)
        latest_posts_data = db.session.query(
            Post.category_id,
            Post.id,
            Post.title,
            Post.created_at
        ).join(
            latest_posts_subquery,
            (Post.category_id == latest_posts_subquery.c.category_id) &
            (Post.created_at == latest_posts_subquery.c.max_created_at)
        ).all()

        # Create a lookup dictionary for latest posts
        latest_posts_map = {
            item.category_id: {
                'id': item.id,
                'title': item.title,
                'created_at': item.created_at
            }
            for item in latest_posts_data
        }

        # Combine results
        category_stats = []
        for category, post_count in results:
            latest_post = latest_posts_map.get(category.id)
            category_stats.append({
                'category': category,
                'post_count': post_count,
                'latest_post': latest_post
            })

        return category_stats

    @staticmethod
    def get_by_id(category_id):
        """
        Get a single category by ID.

        Args:
            category_id (int): Category ID

        Returns:
            Category: Category object or None
        """
        return Category.query.get(category_id)

    @staticmethod
    def get_posts_with_stats(category_id, page=1, per_page=20):
        """
        Get posts in a category with reply counts and latest reply info.
        Uses optimized queries to avoid N+1 problem.

        Args:
            category_id (int): Category ID
            page (int): Page number for pagination
            per_page (int): Number of posts per page

        Returns:
            dict: Dictionary with 'posts', 'total', 'page', 'per_page'
        """
        from app.models import Reply

        # Subquery for reply counts
        reply_counts = db.session.query(
            Reply.post_id,
            func.count(Reply.id).label('reply_count')
        ).group_by(Reply.post_id).subquery()

        # Main query with eager loading
        query = db.session.query(
            Post,
            func.coalesce(reply_counts.c.reply_count, 0).label('reply_count')
        ).outerjoin(
            reply_counts,
            Post.id == reply_counts.c.post_id
        ).filter(
            Post.category_id == category_id
        ).options(
            joinedload(Post.author)  # Eager load author to avoid N+1
        ).order_by(Post.created_at.desc())

        # Get total count for pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * per_page
        results = query.offset(offset).limit(per_page).all()

        # Format results
        posts_with_stats = []
        for post, reply_count in results:
            posts_with_stats.append({
                'post': post,
                'reply_count': reply_count
            })

        return {
            'posts': posts_with_stats,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
