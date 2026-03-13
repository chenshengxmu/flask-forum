from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Post, Reply, Category
from app.forms import PostForm, ReplyForm
from app.utils import save_cover_image, delete_cover_image

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new post"""
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author_id=current_user.id,
            category_id=form.category_id.data
        )
        db.session.add(post)
        db.session.flush()  # Get post.id without committing

        # Handle cover image upload
        if form.cover_image.data:
            filename = save_cover_image(form.cover_image.data, post.id)
            if filename:
                post.cover_image = filename

        db.session.commit()

        flash('Your post has been created!', 'success')
        return redirect(url_for('forum.post', post_id=post.id))

    return render_template('forum/create.html', title='Create Post', form=form)


@posts_bp.route('/<int:post_id>/reply', methods=['POST'])
@login_required
def reply(post_id):
    """Add a reply to a post"""
    post = Post.query.get_or_404(post_id)
    form = ReplyForm()

    if form.validate_on_submit():
        reply = Reply(
            content=form.content.data,
            author_id=current_user.id,
            post_id=post.id
        )
        db.session.add(reply)
        db.session.commit()

        flash('Your reply has been posted!', 'success')
        return redirect(url_for('forum.post', post_id=post.id))

    flash('Error posting reply. Please try again.', 'danger')
    return redirect(url_for('forum.post', post_id=post.id))


@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    """Delete a post (author or admin only)"""
    post = Post.query.get_or_404(post_id)

    if post.author_id != current_user.id and not current_user.is_admin:
        abort(403)

    category_id = post.category_id

    # Delete cover image file if exists
    if post.cover_image:
        delete_cover_image(post.cover_image)

    db.session.delete(post)
    db.session.commit()

    flash('Post has been deleted.', 'success')
    return redirect(url_for('forum.category', category_id=category_id))
