"""Parking Routes — Public parking info"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models.parking_area import ParkingArea
from models.parking_slot import ParkingSlot
from extensions import db

parking_bp = Blueprint('parking', __name__)


@parking_bp.route('/<int:area_id>')
def details(area_id):
    """View parking area details (public)"""
    area = ParkingArea.query.get_or_404(area_id)
    slots = ParkingSlot.query.filter_by(area_id=area_id).all()
    if current_user.is_authenticated:
        return redirect(url_for('user.parking_details', area_id=area_id))
    return render_template('user/parking_details.html', area=area, slots=slots)


@parking_bp.route('/availability/<int:area_id>')
def availability(area_id):
    """JSON endpoint for slot availability"""
    from flask import jsonify
    area = ParkingArea.query.get_or_404(area_id)
    slots = ParkingSlot.query.filter_by(area_id=area_id).all()
    available = [s for s in slots if s.status == 'available']
    return jsonify({
        'area_id': area_id,
        'total': len(slots),
        'available': len(available),
        'slots': [{'id': s.id, 'number': s.slot_number, 'status': s.status} for s in slots]
    })
