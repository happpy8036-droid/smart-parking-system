"""Maps Routes — Google Maps integration"""

from flask import Blueprint, render_template, request

maps_bp = Blueprint('maps', __name__)


@maps_bp.route('/')
def view():
    """Display Google Maps parking location."""

    parking_name = request.args.get('parking_name', 'Smart Parking')
    latitude = request.args.get('lat', '16.9891')
    longitude = request.args.get('lng', '82.2475')

    return render_template(
        'user/parking_map.html',
        parking_name=parking_name,
        latitude=latitude,
        longitude=longitude
    )