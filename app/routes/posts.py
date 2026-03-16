from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Post, Reply, Category
from app.forms import PostForm, ReplyForm
from app.utils import save_cover_image, delete_cover_image
from app.decorators import post_author_or_admin_required
from app.services.post_service import PostService

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new post"""
    from flask import current_app
    form = PostForm()

    if form.validate_on_submit():
        try:
            # Handle cover image upload first
            cover_image_filename = None
            if form.cover_image.data:
                # Create a temporary post ID for image upload
                # We'll use a placeholder and update it after creating the post
                pass

            # Create post using service
            post = PostService.create_post(
                title=form.title.data,
                content=form.content.data,
                author_id=current_user.id,
                category_id=form.category_id.data
            )

            # Handle cover image upload after getting post ID
            if form.cover_image.data:
                filename = save_cover_image(form.cover_image.data, post.id)
                if filename:
                    post.cover_image = filename

            db.session.commit()
            current_app.logger.info(f'User {current_user.username} created post {post.id}: {post.title}')

            flash('Your post has been created!', 'success')
            return redirect(url_for('forum.post', post_id=post.id))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error creating post for user {current_user.username}: {str(e)}', exc_info=True)
            flash('An error occurred while creating your post. Please try again.', 'danger')

    return render_template('forum/create.html', title='Create Post', form=form)


@posts_bp.route('/<int:post_id>/reply', methods=['POST'])
@login_required
def reply(post_id):
    """Add a reply to a post"""
    from flask import current_app
    post = Post.query.get_or_404(post_id)
    form = ReplyForm()

    if form.validate_on_submit():
        try:
            # Create reply using service
            reply = PostService.create_reply(
                content=form.content.data,
                author_id=current_user.id,
                post_id=post.id
            )
            db.session.commit()
            current_app.logger.info(f'User {current_user.username} replied to post {post_id}')

            flash('Your reply has been posted!', 'success')
            return redirect(url_for('forum.post', post_id=post.id))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error posting reply for user {current_user.username} on post {post_id}: {str(e)}', exc_info=True)
            flash('An error occurred while posting your reply. Please try again.', 'danger')
            return redirect(url_for('forum.post', post_id=post.id))

    flash('Error posting reply. Please try again.', 'danger')
    return redirect(url_for('forum.post', post_id=post.id))


@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
@post_author_or_admin_required
def delete(post_id):
    """Delete a post (author or admin only)"""
    from flask import current_app
    post = Post.query.get_or_404(post_id)

    category_id = post.category_id
    post_title = post.title

    try:
        # Delete cover image file if exists
        if post.cover_image:
            delete_cover_image(post.cover_image)

        db.session.delete(post)
        db.session.commit()
        current_app.logger.info(f'User {current_user.username} deleted post {post_id}: {post_title}')

        flash('Post has been deleted.', 'success')
        return redirect(url_for('forum.category', category_id=category_id))

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error deleting post {post_id} by user {current_user.username}: {str(e)}', exc_info=True)
        flash('An error occurred while deleting the post. Please try again.', 'danger')
        return redirect(url_for('forum.post', post_id=post_id))
