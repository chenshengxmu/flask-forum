from flask import Blueprint, render_template, abort
from app.models import Category, Post
from sqlalchemy import desc

forum_bp = Blueprint('forum', __name__)


@forum_bp.route('/')
def index():
    """Homepage displaying all categories"""
    categories = Category.query.order_by(Category.name).all()
    return render_template('index.html', title='BBS Forum', categories=categories)


@forum_bp.route('/category/<int:category_id>')
def category(category_id):
    """Display all posts in a specific category"""
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category_id)\
        .order_by(desc(Post.created_at))\
        .all()
    return render_template('forum/category.html', title=category.name,
                         category=category, posts=posts)


@forum_bp.route('/post/<int:post_id>')
def post(post_id):
    """Display a single post with all replies"""
    from app.forms import ReplyForm
    post = Post.query.get_or_404(post_id)
    replies = post.replies.all()
    form = ReplyForm()
    return render_template('forum/post.html', title=post.title,
                         post=post, replies=replies, form=form)
