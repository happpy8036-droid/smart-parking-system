"""Payment Model — Smart Parking System"""
from extensions import db
from datetime import datetime


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.Enum('card', 'upi', 'netbanking', 'wallet', 'cash'), default='card')
    payment_status = db.Column(db.Enum('pending', 'completed', 'failed', 'refunded'), default='pending')
    transaction_id = db.Column(db.String(100))
    receipt_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    booking = db.relationship('Booking', back_populates='payment')
    user = db.relationship('User', back_populates='payments')

    def __repr__(self):
        return f'<Payment {self.id}>'
