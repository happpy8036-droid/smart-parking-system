"""Auth Routes — Login, Register, Logout"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from models import User, Admin
from utils.helpers import generate_booking_ref
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'user')

        if role == 'admin':
            admin = Admin.query.filter_by(email=email, is_active=1).first()
            if admin and admin.check_password(password):
                login_user(admin)
                flash('Welcome back, Admin!', 'success')
                return redirect(url_for('admin.dashboard'))
            flash('Invalid admin credentials.', 'danger')
        else:
            user = User.query.filter_by(email=email, is_active=1).first()
            if user and user.check_password(password):
                login_user(user)
                flash(f'Welcome back, {user.name}!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('user.dashboard'))
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not all([name, email, phone, password]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('auth/register.html')

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html')

        user = User(name=name, email=email, phone=phone)
        user.set_password(password)

        from extensions import db
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        flash('If an account exists, a reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout and redirect to home"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home.index'))
