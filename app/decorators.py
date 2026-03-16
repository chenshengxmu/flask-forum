"""
Authorization decorators for route protection and access control.
"""
from functools import wraps
from flask import abort, current_app
from flask_login import current_user
from app.models import Post


def admin_required(f):
    """
    Decorator to require admin privileges for a route.

    Usage:
        @app.route('/admin/dashboard')
        @login_required
        @admin_required
        def admin_dashboard():
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            current_app.logger.warning(f'Unauthenticated access attempt to admin route: {f.__name__}')
            abort(401)

        if not current_user.is_admin:
            current_app.logger.warning(
                f'Unauthorized admin access attempt by user {current_user.username} '
                f'to route: {f.__name__}'
            )
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


def post_author_or_admin_required(f):
    """
    Decorator to require that the current user is either the post author or an admin.
    The route must have a 'post_id' parameter.

    Usage:
        @app.route('/posts/<int:post_id>/delete')
        @login_required
        @post_author_or_admin_required
        def delete_post(post_id):
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            current_app.logger.warning(f'Unauthenticated access attempt to protected route: {f.__name__}')
            abort(401)

        # Get post_id from kwargs
        post_id = kwargs.get('post_id')
        if post_id is None:
            current_app.logger.error(f'post_author_or_admin_required used on route without post_id: {f.__name__}')
            abort(500)

        # Check if user is author or admin
        post = Post.query.get_or_404(post_id)

        if post.author_id != current_user.id and not current_user.is_admin:
            current_app.logger.warning(
                f'Unauthorized access attempt by user {current_user.username} '
                f'to post {post_id} (author: {post.author.username})'
            )
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


def permission_required(permission):
    """
    Decorator to require a specific permission for a route.
    This is a flexible decorator that can be extended for role-based access control.

    Args:
        permission (str): The permission name (e.g., 'edit_post', 'delete_user')

    Usage:
        @app.route('/posts/<int:post_id>/edit')
        @login_required
        @permission_required('edit_post')
        def edit_post(post_id):
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                current_app.logger.warning(
                    f'Unauthenticated access attempt to route requiring permission: {permission}'
                )
                abort(401)

            # Check if user has the required permission
            # For now, admins have all permissions
            if not current_user.is_admin:
                # In a more complex system, you would check user.permissions here
                current_app.logger.warning(
                    f'User {current_user.username} lacks permission "{permission}" '
                    f'for route: {f.__name__}'
                )
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def rate_limit_exempt(f):
    """
    Decorator to mark a route as exempt from rate limiting.
    This is a placeholder for future rate limiting implementation.

    Usage:
        @app.route('/health')
        @rate_limit_exempt
        def health_check():
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)

    # Mark the function as rate limit exempt
    decorated_function._rate_limit_exempt = True

    return decorated_function
