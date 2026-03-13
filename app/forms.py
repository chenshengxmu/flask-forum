from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class PostForm(FlaskForm):
    """Form for creating new posts"""
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=5, max=200, message='Title must be between 5 and 200 characters')
    ])
    content = TextAreaField('Content', validators=[
        DataRequired(),
        Length(min=10, message='Content must be at least 10 characters')
    ])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    cover_image = FileField('Cover Image (Optional)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'],
                   'Images only! Allowed: jpg, jpeg, png, gif, webp')
    ])

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        from app.models import Category
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]


class ReplyForm(FlaskForm):
    """Form for replying to posts"""
    content = TextAreaField('Reply', validators=[
        DataRequired(),
        Length(min=5, message='Reply must be at least 5 characters')
    ])


class CategoryForm(FlaskForm):
    """Form for creating/editing categories (admin only)"""
    name = StringField('Category Name', validators=[
        DataRequired(),
        Length(min=3, max=100, message='Category name must be between 3 and 100 characters')
    ])
    description = TextAreaField('Description', validators=[
        Length(max=500, message='Description cannot exceed 500 characters')
    ])
