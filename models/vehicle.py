"""Vehicle Model — Smart Parking System"""
from extensions import db
from datetime import datetime


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_number = db.Column(db.String(50), nullable=False)
    vehicle_type = db.Column(db.Enum('car', 'bike', 'suv', 'truck', 'ev'), default='car')
    color = db.Column(db.String(50))
    brand = db.Column(db.String(100))
    is_default = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='vehicles')
    bookings = db.relationship('Booking', back_populates='vehicle')

    def __repr__(self):
        return f'<Vehicle {self.vehicle_number}>'
