"""
Seed Script — Smart Parking System
Run this AFTER the app starts to create default admin and demo users
with proper Werkzeug password hashes.

Usage: python seed_script.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

from werkzeug.security import generate_password_hash
from app import create_app
from extensions import db
from models.admin import Admin
from models.user import User

app = create_app()

with app.app_context():
    # Check if admin exists
    admin = Admin.query.filter_by(email='admin@smartparking.com').first()
    if not admin:
        admin = Admin(name='Admin', email='admin@smartparking.com')
        admin.set_password('admin@1234')
        db.session.add(admin)
        db.session.commit()
        print('[OK] Admin user created: admin@smartparking.com / admin@1234')
    else:
        print('[SKIP] Admin already exists. Updating password...')
        admin.set_password('admin@1234')
        db.session.commit()
        print('[OK] Admin password reset to: admin@1234')

    # Check if demo users exist
    rahul = User.query.filter_by(email='rahul@example.com').first()
    if not rahul:
        rahul = User(name='Rahul Sharma', email='rahul@example.com', phone='9876543210')
        rahul.set_password('password123')
        db.session.add(rahul)
        db.session.commit()
        print('[OK] Demo user created: rahul@example.com / password123')
    else:
        print('[SKIP] Demo user rahul@example.com already exists.')

    priya = User.query.filter_by(email='priya@example.com').first()
    if not priya:
        priya = User(name='Priya Patel', email='priya@example.com', phone='9876543211')
        priya.set_password('password123')
        db.session.add(priya)
        db.session.commit()
        print('[OK] Demo user created: priya@example.com / password123')
    else:
        print('[SKIP] Demo user priya@example.com already exists.')

    print('\n--- Login Credentials ---')
    print('Admin: admin@smartparking.com / admin@1234')
    print('User:  rahul@example.com / password123')
    print('User:  priya@example.com / password123')
