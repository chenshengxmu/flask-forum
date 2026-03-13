from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Import models here to avoid circular imports
    from app import models

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.forum import forum_bp
    from app.routes.posts import posts_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(posts_bp)

    # Setup Flask-Admin
    from app.routes.admin import setup_admin
    setup_admin(app)

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('500.html'), 500

    return app
