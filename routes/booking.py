"""Booking Routes — Slot booking and payment"""

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session
)

from flask_login import login_required, current_user

from models.parking_area import ParkingArea
from models.parking_slot import ParkingSlot
from models.booking import Booking
from models.vehicle import Vehicle

from extensions import db
from datetime import datetime, timedelta

from utils.helpers import generate_booking_ref


booking_bp = Blueprint('booking', __name__)


# ==========================================================
# CREATE BOOKING
# ==========================================================

@booking_bp.route('/<int:area_id>', methods=['GET', 'POST'])
@login_required
def create(area_id):
    """Show booking form and prepare payment"""

    area = ParkingArea.query.get_or_404(area_id)

    # Get selected slot
    slot_id = (
        request.args.get('slot', type=int)
        or request.form.get('slot_id', type=int)
    )

    # ======================================================
    # POST — VALIDATE BOOKING DETAILS
    # ======================================================

    if request.method == 'POST':

        if not slot_id:
            flash('Please select a parking slot.', 'danger')
            return redirect(
                url_for(
                    'user.parking_details',
                    area_id=area_id
                )
            )

        # Get slot
        slot = ParkingSlot.query.get(slot_id)

        if not slot:
            flash('Parking slot not found.', 'danger')
            return redirect(
                url_for(
                    'user.parking_details',
                    area_id=area_id
                )
            )

        # Check slot belongs to selected area
        if slot.area_id != area_id:
            flash('Invalid parking slot.', 'danger')
            return redirect(
                url_for(
                    'user.parking_details',
                    area_id=area_id
                )
            )

        # Check slot availability
        if slot.status != 'available':
            flash('This parking slot is no longer available.', 'danger')
            return redirect(
                url_for(
                    'user.parking_details',
                    area_id=area_id
                )
            )

        # ==================================================
        # GET FORM DATA
        # ==================================================

        booking_date = request.form.get(
            'booking_date',
            datetime.now().strftime('%Y-%m-%d')
        )

        start_time = request.form.get(
            'start_time',
            '09:00'
        )

        try:
            hours = int(
                request.form.get('hours', 1)
            )
        except (TypeError, ValueError):
            hours = 1

        # Minimum 1 hour
        if hours < 1:
            hours = 1

        # Maximum 24 hours
        if hours > 24:
            hours = 24

        # Vehicle
        vehicle_id = request.form.get(
            'vehicle_id',
            type=int
        )

        # Notes
        notes = request.form.get(
            'notes',
            ''
        ).strip()

        # ==================================================
        # CALCULATE AMOUNT
        # ==================================================

        price_per_hour = float(
            slot.price_per_hour or 0
        )

        total_amount = hours * price_per_hour

        duration_minutes = hours * 60

        # ==================================================
        # CALCULATE END TIME
        # ==================================================

        try:
            start_dt = datetime.strptime(
                start_time,
                '%H:%M'
            )

            end_dt = (
                start_dt +
                timedelta(minutes=duration_minutes)
            )

            end_time = end_dt.strftime('%H:%M')

        except ValueError:
            flash(
                'Invalid start time.',
                'danger'
            )

            return redirect(
                url_for(
                    'booking.create',
                    area_id=area_id,
                    slot=slot_id
                )
            )

        # ==================================================
        # SAVE TEMPORARY BOOKING DATA IN SESSION
        # ==================================================

        session['pending_booking'] = {
            'area_id': area_id,
            'slot_id': slot.id,
            'vehicle_id': vehicle_id,
            'booking_date': booking_date,
            'start_time': start_time,
            'end_time': end_time,
            'hours': hours,
            'duration': duration_minutes,
            'total_amount': total_amount,
            'notes': notes
        }

        # ==================================================
        # GO TO PAYMENT PAGE
        # ==================================================

        return redirect(
            url_for(
                'user.payment'
            )
        )

    # ======================================================
    # GET — SHOW BOOKING FORM
    # ======================================================

    slot = (
        ParkingSlot.query.get_or_404(slot_id)
        if slot_id
        else None
    )

    vehicles = Vehicle.query.filter_by(
        user_id=current_user.id
    ).all()

    today = datetime.now().strftime(
        '%Y-%m-%d'
    )

    return render_template(
        'user/booking.html',
        area=area,
        slot=slot,
        vehicles=vehicles,
        today=today
    )


# ==========================================================
# CANCEL BOOKING
# ==========================================================

@booking_bp.route(
    '/cancel/<int:booking_id>',
    methods=['POST']
)
@login_required
def cancel(booking_id):
    """Cancel a booking"""

    booking = Booking.query.get_or_404(
        booking_id
    )

    # Security check
    if booking.user_id != current_user.id:
        flash(
            'Access denied.',
            'danger'
        )

        return redirect(
            url_for('user.booking_history')
        )

    # Check status
    if booking.status != 'confirmed':
        flash(
            'This booking cannot be cancelled.',
            'danger'
        )

        return redirect(
            url_for(
                'user.booking_details',
                booking_id=booking.id
            )
        )

    # ======================================================
    # CANCEL BOOKING
    # ======================================================

    booking.status = 'cancelled'

    # Free slot
    slot = ParkingSlot.query.get(
        booking.slot_id
    )

    if slot:
        slot.status = 'available'

    # Update parking area
    area = ParkingArea.query.get(
        booking.area_id
    )

    if area:
        area.available_slots = min(
            area.total_slots,
            area.available_slots + 1
        )

    db.session.commit()

    flash(
        'Booking cancelled successfully.',
        'success'
    )

    return redirect(
        url_for('user.booking_history')
    )