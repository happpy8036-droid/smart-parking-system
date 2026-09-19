"""Notification Model — Smart Parking System"""
from extensions import db
from datetime import datetime


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Integer, default=0)
    notification_type = db.Column(db.Enum('booking', 'payment', 'system', 'promotion'), default='system')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='notifications')

    def __repr__(self):
        return f'<Notification {self.id}>'
