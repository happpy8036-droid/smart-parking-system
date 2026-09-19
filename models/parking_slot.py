"""Parking Slot Model — Smart Parking System"""
from extensions import db
from datetime import datetime


class ParkingSlot(db.Model):
    __tablename__ = 'parking_slots'

    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('parking_areas.id'), nullable=False)
    slot_number = db.Column(db.String(50), nullable=False)
    slot_type = db.Column(db.Enum('standard', 'premium', 'ev_charging', 'handicap', 'bike'), default='standard')
    status = db.Column(db.Enum('available', 'occupied', 'reserved', 'maintenance'), default='available')
    price_per_hour = db.Column(db.Float, nullable=False, default=50.00)
    is_special = db.Column(db.Integer, default=0)
    row = db.Column(db.String(10))
    col = db.Column(db.Integer)
    floor = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bookings = db.relationship('Booking', back_populates='slot', lazy=True)
    area = db.relationship('ParkingArea', back_populates='slots')

    def __repr__(self):
        return f'<ParkingSlot {self.slot_number}>'
