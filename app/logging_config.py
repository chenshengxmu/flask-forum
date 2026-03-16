"""
Centralized logging configuration for the BBS Forum application.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import request, has_request_context
import time


class RequestFormatter(logging.Formatter):
    """Custom formatter that includes request context information."""

    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method
            record.request_id = getattr(request, 'request_id', 'N/A')
        else:
            record.url = 'N/A'
            record.remote_addr = 'N/A'
            record.method = 'N/A'
            record.request_id = 'N/A'

        return super().format(record)


def setup_logging(app):
    """
    Configure application logging with separate handlers for different log levels.

    Args:
        app: Flask application instance
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(app.root_path, '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Set base logging level from config
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    app.logger.setLevel(getattr(logging, log_level))

    # Remove default handlers
    app.logger.handlers.clear()

    # Console handler for development
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        app.logger.addHandler(console_handler)

    # General application log (INFO and above)
    app_log_file = os.path.join(log_dir, 'app.log')
    app_handler = RotatingFileHandler(
        app_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    app_handler.setLevel(logging.INFO)
    app_formatter = RequestFormatter(
        '[%(asctime)s] %(levelname)s [%(request_id)s] %(remote_addr)s - '
        '%(method)s %(url)s - %(message)s'
    )
    app_handler.setFormatter(app_formatter)
    app.logger.addHandler(app_handler)

    # Error log (ERROR and above)
    error_log_file = os.path.join(log_dir, 'error.log')
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = RequestFormatter(
        '[%(asctime)s] %(levelname)s [%(request_id)s] %(remote_addr)s - '
        '%(method)s %(url)s\n'
        'Message: %(message)s\n'
        'Location: %(pathname)s:%(lineno)d\n'
    )
    error_handler.setFormatter(error_formatter)
    app.logger.addHandler(error_handler)

    # Database query log (optional, for debugging)
    if app.config.get('LOG_SQL_QUERIES', False):
        db_log_file = os.path.join(log_dir, 'database.log')
        db_handler = RotatingFileHandler(
            db_log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        db_handler.setLevel(logging.DEBUG)
        db_formatter = logging.Formatter(
            '[%(asctime)s] %(message)s'
        )
        db_handler.setFormatter(db_formatter)

        # Configure SQLAlchemy logging
        sql_logger = logging.getLogger('sqlalchemy.engine')
        sql_logger.setLevel(logging.DEBUG)
        sql_logger.addHandler(db_handler)

    # Access log (all requests)
    access_log_file = os.path.join(log_dir, 'access.log')
    access_handler = RotatingFileHandler(
        access_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    access_handler.setLevel(logging.INFO)
    access_formatter = logging.Formatter(
        '[%(asctime)s] %(remote_addr)s - "%(method)s %(url)s" '
        '%(status_code)s %(response_time)sms'
    )
    access_handler.setFormatter(access_formatter)

    # Create access logger
    access_logger = logging.getLogger('access')
    access_logger.setLevel(logging.INFO)
    access_logger.addHandler(access_handler)

    # Register request logging middleware
    @app.before_request
    def before_request():
        """Add request ID and start time to request context."""
        request.request_id = generate_request_id()
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        """Log request details after processing."""
        if request.endpoint != 'static':
            response_time = int((time.time() - request.start_time) * 1000)
            access_logger.info(
                '',
                extra={
                    'remote_addr': request.remote_addr,
                    'method': request.method,
                    'url': request.url,
                    'status_code': response.status_code,
                    'response_time': response_time
                }
            )
        return response

    app.logger.info('Logging initialized')


def generate_request_id():
    """Generate a unique request ID for tracking."""
    import uuid
    return str(uuid.uuid4())[:8]
