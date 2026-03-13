from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model for authentication and post authorship"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    replies = db.relationship('Reply', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """Category model for organizing posts into sections"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cover_image = db.Column(db.String(255), nullable=True)

    # Relationships
    posts = db.relationship('Post', backref='category', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def post_count(self):
        """Get total number of posts in this category"""
        return self.posts.count()

    @property
    def latest_post(self):
        """Get the most recent post in this category"""
        return self.posts.order_by(Post.created_at.desc()).first()

    def __repr__(self):
        return f'<Category {self.name}>'


class Post(db.Model):
    """Post model for forum threads"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    cover_image = db.Column(db.String(255), nullable=True)

    # Relationships
    replies = db.relationship('Reply', backref='post', lazy='dynamic',
                            cascade='all, delete-orphan', order_by='Reply.created_at')

    @property
    def reply_count(self):
        """Get total number of replies to this post"""
        return self.replies.count()

    @property
    def latest_reply(self):
        """Get the most recent reply to this post"""
        return self.replies.order_by(Reply.created_at.desc()).first()

    def __repr__(self):
        return f'<Post {self.title}>'


class Reply(db.Model):
    """Reply model for responses to posts"""
    __tablename__ = 'replies'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f'<Reply to Post {self.post_id}>'
