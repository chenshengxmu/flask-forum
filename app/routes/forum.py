from flask import Blueprint, render_template, abort, current_app
from app.models import Category, Post
from app.services.category_service import CategoryService
from app.services.post_service import PostService
from sqlalchemy import desc

forum_bp = Blueprint('forum', __name__)


@forum_bp.route('/')
def index():
    """Homepage displaying all categories with optimized queries"""
    category_stats = CategoryService.get_all_with_stats()
    return render_template('index.html', title='BBS Forum', category_stats=category_stats)


@forum_bp.route('/category/<int:category_id>')
def category(category_id):
    """Display posts in a specific category with pagination"""
    from flask import request

    category = CategoryService.get_by_id(category_id)
    if not category:
        abort(404)

    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 20)

    # Get posts with stats using optimized query
    result = CategoryService.get_posts_with_stats(category_id, page=page, per_page=per_page)

    return render_template('forum/category.html',
                         title=category.name,
                         category=category,
                         posts_data=result['posts'],
                         pagination=result)


@forum_bp.route('/post/<int:post_id>')
def post(post_id):
    """Display a single post with paginated replies"""
    from app.forms import ReplyForm
    from flask import request

    # Get post with eager loaded relations
    post = PostService.get_by_id_with_relations(post_id)
    if not post:
        abort(404)

    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('REPLIES_PER_PAGE', 50)

    # Get paginated replies with optimized query
    result = PostService.get_replies_paginated(post_id, page=page, per_page=per_page)

    form = ReplyForm()
    return render_template('forum/post.html',
                         title=post.title,
                         post=post,
                         replies=result['replies'],
                         pagination=result,
                         form=form)
