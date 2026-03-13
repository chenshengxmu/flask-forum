from flask import redirect, url_for, request
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app import db
from app.models import User, Category, Post, Reply


class SecureModelView(ModelView):
    """Base model view with admin authentication"""

    def is_accessible(self):
        """Only allow access to admin users"""
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to login page if user doesn't have access"""
        return redirect(url_for('auth.login', next=request.url))


class UserAdminView(SecureModelView):
    """Admin view for User model"""
    column_list = ['id', 'username', 'email', 'is_admin', 'created_at']
    column_searchable_list = ['username', 'email']
    column_filters = ['is_admin', 'created_at']
    form_excluded_columns = ['password_hash', 'posts', 'replies']
    can_create = False
    can_edit = True
    can_delete = True


class CategoryAdminView(SecureModelView):
    """Admin view for Category model"""
    column_list = ['id', 'name', 'description', 'created_at']
    column_searchable_list = ['name', 'description']
    form_excluded_columns = ['posts']
    can_create = True
    can_edit = True
    can_delete = True


class PostAdminView(SecureModelView):
    """Admin view for Post model"""
    column_list = ['id', 'title', 'author', 'category', 'created_at']
    column_searchable_list = ['title', 'content']
    column_filters = ['created_at']
    form_excluded_columns = ['replies']
    can_create = False
    can_edit = True
    can_delete = True


class ReplyAdminView(SecureModelView):
    """Admin view for Reply model"""
    column_list = ['id', 'author', 'post', 'created_at']
    column_searchable_list = ['content']
    column_filters = ['created_at']
    can_create = False
    can_edit = True
    can_delete = True


class SecureAdminIndexView(AdminIndexView):
    """Secure admin index view"""

    @expose('/')
    def index(self):
        """Admin dashboard"""
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('auth.login', next=request.url))
        return super(SecureAdminIndexView, self).index()


def setup_admin(app):
    """Initialize Flask-Admin with the app"""
    admin = Admin(
        app,
        name='BBS Forum Admin',
        template_mode='bootstrap4',
        index_view=SecureAdminIndexView()
    )

    # Add model views
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(CategoryAdminView(Category, db.session))
    admin.add_view(PostAdminView(Post, db.session))
    admin.add_view(ReplyAdminView(Reply, db.session))
