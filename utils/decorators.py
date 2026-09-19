"""Decorators — Smart Parking System"""
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if current user is an Admin by class name
        if current_user.__class__.__name__ != 'Admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def premium_required(f):
    """Decorator to require premium user role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from models import User
        if isinstance(current_user, User) and current_user.role != 'premium':
            flash('Premium membership required.', 'warning')
            return redirect(url_for('user.dashboard'))
        return f(*args, **kwargs)
    return decorated_function
