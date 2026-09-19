"""
Smart Parking System — Main Flask Application
A complete parking slot booking platform like BookMyShow
"""
import os
from flask import Flask, render_template, flash, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

from extensions import db, login_manager, mail


def create_app():
    """Application factory — creates and configures the Flask app"""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    db_user = os.getenv('DB_USER', 'root')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'smart_parking_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{db_user}:{os.getenv('DB_PASSWORD', '')}@"
        f"{db_host}:{db_port}/{db_name}"
    )
    print(f"[SmartParking] Project: {os.path.abspath(__file__)}")
    print(f"[SmartParking] Database target: {db_user}@{db_host}:{db_port}/{db_name}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from routes.home import home_bp
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.admin import admin_bp
    from routes.parking import parking_bp
    from routes.booking import booking_bp
    from routes.payment import payment_bp
    from routes.maps import maps_bp
    from routes.api import api_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(parking_bp, url_prefix='/parking')
    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(payment_bp, url_prefix='/payment')
    app.register_blueprint(maps_bp, url_prefix='/maps')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Create tables if they don't exist
    with app.app_context():
        # Import models AFTER db.init_app so they bind correctly
        from models.user import User
        from models.admin import Admin
        from models.vehicle import Vehicle
        from models.parking_area import ParkingArea
        from models.parking_slot import ParkingSlot
        from models.booking import Booking
        from models.payment import Payment
        from models.notification import Notification
        from models.feedback import Feedback
        from models.activity_log import ActivityLog
        db.create_all()

    # User loader for Flask-Login
    # Admin IDs prefixed with 'admin_' to distinguish from User IDs
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        from models.admin import Admin
        if user_id.startswith('admin_'):
            admin_id = int(user_id.split('admin_')[1])
            return Admin.query.get(admin_id)
        else:
            return User.query.get(int(user_id))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
