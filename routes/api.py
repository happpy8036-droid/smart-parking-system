"""API Routes — JSON endpoints for AJAX"""
from flask import Blueprint, jsonify
from models.parking_area import ParkingArea
from models.parking_slot import ParkingSlot

api_bp = Blueprint('api', __name__)


@api_bp.route('/areas')
def list_areas():
    """Get all parking areas as JSON"""
    areas = ParkingArea.query.filter_by(is_active=1).all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'city': a.city,
        'area': a.area,
        'total_slots': a.total_slots,
        'available_slots': a.available_slots,
        'price_per_hour': a.price_per_hour
    } for a in areas])


@api_bp.route('/areas/<int:area_id>/slots')
def list_slots(area_id):
    """Get slots for a parking area as JSON"""
    slots = ParkingSlot.query.filter_by(area_id=area_id).all()
    return jsonify([{
        'id': s.id,
        'slot_number': s.slot_number,
        'slot_type': s.slot_type,
        'status': s.status,
        'price_per_hour': s.price_per_hour
    } for s in slots])
