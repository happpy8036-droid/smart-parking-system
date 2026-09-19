"""Admin Model — Smart Parking System"""
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'super_admin'), default='admin')
    is_active = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        """Return prefixed ID so Flask-Login knows this is an admin"""
        return f'admin_{self.id}'

    def __repr__(self):
        return f'<Admin {self.email}>'
