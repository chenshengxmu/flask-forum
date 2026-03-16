from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    from flask import current_app
    from sqlalchemy.exc import IntegrityError

    if current_user.is_authenticated:
        return redirect(url_for('forum.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(f'New user registered: {user.username}')

            flash('Congratulations, you are now registered! Please log in.', 'success')
            return redirect(url_for('auth.login'))

        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.warning(f'Registration failed - duplicate username/email: {form.username.data}')
            flash('Username or email already exists. Please choose a different one.', 'danger')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error during registration: {str(e)}', exc_info=True)
            flash('An error occurred during registration. Please try again.', 'danger')

    return render_template('auth/register.html', title='Register', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    from flask import current_app

    if current_user.is_authenticated:
        return redirect(url_for('forum.index'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()

            if user is None or not user.check_password(form.password.data):
                current_app.logger.warning(f'Failed login attempt for username: {form.username.data} from IP: {request.remote_addr}')
                flash('Invalid username or password', 'danger')
                return redirect(url_for('auth.login'))

            login_user(user, remember=form.remember_me.data)
            current_app.logger.info(f'User {user.username} logged in from IP: {request.remote_addr}')
            flash(f'Welcome back, {user.username}!', 'success')

            # Redirect to next page if it exists, otherwise go to index
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('forum.index'))

        except Exception as e:
            current_app.logger.error(f'Error during login: {str(e)}', exc_info=True)
            flash('An error occurred during login. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/logout')
def logout():
    """User logout"""
    from flask import current_app

    username = current_user.username if current_user.is_authenticated else 'Unknown'
    logout_user()
    current_app.logger.info(f'User {username} logged out')
    flash('You have been logged out.', 'info')
    return redirect(url_for('forum.index'))
