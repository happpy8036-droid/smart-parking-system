"""
Shared Flask extensions — Smart Parking System
All extensions are created here so models and routes can import them
without causing circular import errors.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

# Configure login manager defaults
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'warning'
