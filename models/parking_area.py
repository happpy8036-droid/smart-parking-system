"""Parking Area Model — Smart Parking System"""
from extensions import db
from datetime import datetime


class ParkingArea(db.Model):
    __tablename__ = 'parking_areas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    price_per_hour = db.Column(db.Float, nullable=False, default=50.00)
    open_time = db.Column(db.String(10), nullable=False, default='00:00')
    close_time = db.Column(db.String(10), nullable=False, default='23:59')
    total_slots = db.Column(db.Integer, nullable=False, default=0)
    available_slots = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    slots = db.relationship('ParkingSlot', back_populates='area', lazy=True)
    bookings = db.relationship('Booking', back_populates='area', lazy=True)

    def __repr__(self):
        return f'<ParkingArea {self.name}>'
