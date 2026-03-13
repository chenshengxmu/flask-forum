import os
from app import create_app, db
from app.models import User, Category, Post, Reply

app = create_app(os.getenv('FLASK_ENV', 'default'))


@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'Category': Category,
        'Post': Post,
        'Reply': Reply
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
