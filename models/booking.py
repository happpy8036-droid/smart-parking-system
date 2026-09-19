"""Booking Model — Smart Parking System"""
from extensions import db
from datetime import datetime


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('parking_areas.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('parking_slots.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    booking_date = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=60)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('confirmed', 'completed', 'cancelled', 'no_show'), default='confirmed')
    booking_ref = db.Column(db.String(20), unique=True, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='bookings')
    area = db.relationship('ParkingArea', back_populates='bookings')
    slot = db.relationship('ParkingSlot', back_populates='bookings')
    vehicle = db.relationship('Vehicle', back_populates='bookings')
    payment = db.relationship('Payment', back_populates='booking', uselist=False)
    feedbacks = db.relationship('Feedback', back_populates='booking', lazy=True)

    def __repr__(self):
        return f'<Booking {self.booking_ref}>'
