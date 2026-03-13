# BBS Forum

A classic Bulletin Board System (BBS) forum built with Flask and SQLite.

## Features

- **User Authentication**: Register, login, and logout functionality
- **Post & Reply System**: Create posts and reply to discussions
- **Categories**: Organize posts into different sections
- **Admin Panel**: Flask-Admin interface for managing users, categories, posts, and replies
- **Responsive Design**: Bootstrap 5 for mobile-friendly interface
- **SQLite Database**: Simple, file-based database with no setup required

## Technology Stack

- **Backend**: Python 3.8+ with Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **Admin**: Flask-Admin
- **Frontend**: Jinja2 templates with Bootstrap 5

## Installation

1. **Clone or navigate to the project directory**

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Create an admin user (optional)**
   ```bash
   python3 -c "from app import create_app, db; from app.models import User; app = create_app(); app.app_context().push(); admin = User(username='admin', email='admin@example.com', is_admin=True); admin.set_password('admin123'); db.session.add(admin); db.session.commit(); print('Admin user created!')"
   ```

6. **Create some initial categories**
   ```bash
   python3 -c "from app import create_app, db; from app.models import Category; app = create_app(); app.app_context().push(); categories = [Category(name='General Discussion', description='General topics and discussions'), Category(name='Technology', description='Tech news, programming, and software'), Category(name='Off-Topic', description='Everything else')]; db.session.add_all(categories); db.session.commit(); print('Categories created!')"
   ```

## Running the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Usage

### For Regular Users

1. **Register**: Create a new account at `/auth/register`
2. **Login**: Sign in at `/auth/login`
3. **Browse**: View categories and posts on the homepage
4. **Create Posts**: Click "Create Post" in the navigation bar
5. **Reply**: Click on a post to view it and add replies

### For Administrators

1. **Access Admin Panel**: Navigate to `/admin` (requires admin privileges)
2. **Manage Categories**: Create, edit, or delete categories
3. **Manage Users**: View users, promote to admin, or delete accounts
4. **Manage Content**: Edit or delete posts and replies

## Project Structure

```
bbs-forum/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── models.py             # Database models
│   ├── forms.py              # WTForms for user input
│   ├── routes/               # Route blueprints
│   │   ├── auth.py           # Authentication routes
│   │   ├── forum.py          # Forum browsing routes
│   │   ├── posts.py          # Post creation and reply routes
│   │   └── admin.py          # Admin panel setup
│   ├── templates/            # Jinja2 HTML templates
│   └── static/               # CSS, JS, images
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
└── README.md                 # This file
```

## Database Schema

- **User**: id, username, email, password_hash, is_admin, created_at
- **Category**: id, name, description, created_at
- **Post**: id, title, content, author_id, category_id, created_at, updated_at
- **Reply**: id, content, author_id, post_id, created_at

## Security Features

- Password hashing using Werkzeug
- CSRF protection via Flask-WTF
- SQL injection prevention via SQLAlchemy ORM
- Session management with Flask-Login
- Admin-only access control for administrative functions

## License

MIT License - feel free to use this project for learning or personal use.
