import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bbs_forum.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Flask-Admin configuration
    FLASK_ADMIN_SWATCH = 'cerulean'

    # Pagination
    POSTS_PER_PAGE = 20
    REPLIES_PER_PAGE = 50

    # File upload configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads/covers')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
