"""User Routes — Dashboard, Profile, Vehicles, Search, Booking History"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, session
import qrcode
import io
import uuid
from sqlalchemy import or_
from flask_login import login_required, current_user
from models import User, Booking, ParkingArea, Notification, Feedback, Payment, ParkingSlot, Vehicle
from extensions import db
from utils.helpers import generate_booking_ref
from datetime import datetime

user_bp = Blueprint('user', __name__)
# ==========================================================
# AUTO COMPLETE EXPIRED BOOKINGS
# ==========================================================

def auto_complete_expired_bookings():
    """
    Automatically completes bookings whose date and end time
    have already passed, and releases the parking slot.
    """

    now = datetime.now()

    active_bookings = Booking.query.filter_by(
        status='confirmed'
    ).all()

    changed = False

    for booking in active_bookings:

        booking_datetime = None

        # Try common date formats
        date_formats = [
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%Y/%m/%d'
        ]

        time_formats = [
            '%H:%M',
            '%I:%M %p',
            '%I:%M%p'
        ]

        for date_format in date_formats:

            if booking_datetime:
                break

            for time_format in time_formats:

                try:
                    booking_datetime = datetime.strptime(
                        f"{booking.booking_date} {booking.end_time}",
                        f"{date_format} {time_format}"
                    )

                    break

                except ValueError:
                    continue

        # Skip if date/time format could not be understood
        if not booking_datetime:
            print(
                "Could not parse booking date/time:",
                booking.id,
                booking.booking_date,
                booking.end_time
            )
            continue

        # ==================================================
        # BOOKING TIME COMPLETED
        # ==================================================

        if now >= booking_datetime:

            print(
                f"Booking {booking.id} expired. "
                f"Releasing slot {booking.slot_id}."
            )

            # Mark booking completed
            booking.status = 'completed'

            # Get parking slot
            slot = ParkingSlot.query.get(
                booking.slot_id
            )

            if slot:

                # Check whether another confirmed booking
                # is still using this slot
                other_active = Booking.query.filter(
                    Booking.slot_id == booking.slot_id,
                    Booking.status == 'confirmed',
                    Booking.id != booking.id
                ).all()

                slot_still_occupied = False

                for other_booking in other_active:

                    other_datetime = None

                    for date_format in date_formats:

                        if other_datetime:
                            break

                        for time_format in time_formats:

                            try:
                                other_datetime = datetime.strptime(
                                    f"{other_booking.booking_date} "
                                    f"{other_booking.end_time}",
                                    f"{date_format} {time_format}"
                                )
                                break

                            except ValueError:
                                continue

                    if other_datetime and other_datetime > now:
                        slot_still_occupied = True
                        break

                # Release slot only if no active booking exists
                if not slot_still_occupied:

                    slot.status = 'available'

                    # Increase available slot count
                    area = ParkingArea.query.get(
                        booking.area_id
                    )

                    if area:

                        total_slots = len(area.slots)

                        area.available_slots = min(
                            total_slots,
                            area.available_slots + 1
                        )

            changed = True

    if changed:

        try:
            db.session.commit()

        except Exception as e:

            db.session.rollback()

            print(
                "AUTO BOOKING UPDATE ERROR:",
                e
            )


# Run automatic booking check before user requests
@user_bp.before_request
def check_expired_bookings():

    try:
        auto_complete_expired_bookings()

    except Exception as e:

        print(
            "AUTO BOOKING CHECK ERROR:",
            e
        )

@user_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with stats"""
    if isinstance(current_user, User) and not hasattr(current_user, 'id'):
        return redirect(url_for('auth.login'))
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).limit(5).all()
    total_bookings = Booking.query.filter_by(user_id=current_user.id).count()
    active_bookings = Booking.query.filter_by(user_id=current_user.id, status='confirmed').count()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=0).order_by(Notification.created_at.desc()).limit(5).all()
    return render_template('user/dashboard.html', bookings=bookings, total_bookings=total_bookings,
                           active_bookings=active_bookings, notifications=notifications)


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name)
        current_user.phone = request.form.get('phone', current_user.phone)
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user.profile'))
    return render_template('user/profile.html')


@user_bp.route('/vehicles')
@login_required
def vehicles():
    """List user vehicles"""
    user_vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    return render_template('user/vehicles.html', vehicles=user_vehicles)


@user_bp.route('/vehicles/<int:vehicle_id>')
@login_required
def vehicle_details(vehicle_id):
    """View vehicle details"""
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if vehicle.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('user.vehicles'))
    return render_template('user/vehicle_details.html', vehicle=vehicle)


@user_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_parking():
    """Search parking locations"""

    query = request.args.get('q', '').strip()

    if not query:
        results = ParkingArea.query.filter(
            ParkingArea.is_active == 1
        ).all()
    else:
        search_term = f"%{query}%"

        results = ParkingArea.query.filter(
            or_(
                ParkingArea.name.ilike(search_term),
                ParkingArea.city.ilike(search_term),
                ParkingArea.area.ilike(search_term)
            )
        ).all()

    print("SEARCH:", query)
    print("RESULT COUNT:", len(results))

    for r in results:
        print("FOUND:", r.id, r.name, r.city, r.area, r.is_active)

    return render_template(
        'user/search_parking.html',
        results=results,
        query=query
    )
@user_bp.route('/parking-list')
@login_required
def parking_list():
    """List all parking areas"""
    page = request.args.get('page', 1, type=int)
    areas = ParkingArea.query.filter_by(is_active=1).paginate(page=page, per_page=10, error_out=False)
    return render_template('user/parking_list.html', areas=areas)


@user_bp.route('/parking/<int:area_id>')
@login_required
def parking_details(area_id):
    """View parking area details with zones"""
    area = ParkingArea.query.get_or_404(area_id)
    slots = ParkingArea.query.get(area_id).slots
    return render_template('user/parking_details.html', area=area, slots=slots)


@user_bp.route('/booking-history')
@login_required
def booking_history():
    """View all user bookings"""
    status_filter = request.args.get('status', '')
    query = Booking.query.filter_by(user_id=current_user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
    bookings = query.order_by(Booking.created_at.desc()).all()
    return render_template('user/booking_history.html', bookings=bookings, status_filter=status_filter)


@user_bp.route('/booking/<int:booking_id>')
@login_required
def booking_details(booking_id):
    """View booking details"""
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('user.booking_history'))
    return render_template('user/booking_details.html', booking=booking)


@user_bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel a booking"""
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('user.booking_history'))
    if booking.status != 'confirmed':
        flash('This booking cannot be cancelled.', 'danger')
        return redirect(url_for('user.booking_details', booking_id=booking.id))

    booking.status = 'cancelled'
    # Free the slot
    slot = ParkingArea.query.get(booking.area_id).slots
    from models import ParkingSlot
    slot_obj = ParkingSlot.query.get(booking.slot_id)
    if slot_obj:
        slot_obj.status = 'available'
    db.session.commit()
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('user.booking_details', booking_id=booking.id))


@user_bp.route('/notifications')
@login_required
def notifications():
    """View user notifications"""
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    # Mark all as read
    Notification.query.filter_by(user_id=current_user.id, is_read=0).update({'is_read': 1})
    db.session.commit()
    return render_template('user/notifications.html', notifications=notifs)


@user_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    """Submit feedback"""
    if request.method == 'POST':
        rating = int(request.form.get('rating', 0))
        comment = request.form.get('comment', '')
        booking_id = request.form.get('booking_id', type=int)
        fb = Feedback(user_id=current_user.id, rating=rating, comment=comment, booking_id=booking_id)
        db.session.add(fb)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('user.dashboard'))
    bookings = Booking.query.filter_by(user_id=current_user.id, status='completed').all()
    return render_template('user/feedback.html', bookings=bookings)


@user_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """User settings page"""
    if request.method == 'POST':
        flash('Settings saved.', 'success')
    return render_template('user/settings.html')
@user_bp.route('/booking/<int:booking_id>/qr')
@login_required
def booking_qr(booking_id):

    booking = Booking.query.filter_by(
        id=booking_id,
        user_id=current_user.id
    ).first_or_404()

    # Slot
    slot_number = "N/A"
    if booking.slot:
        slot_number = booking.slot.slot_number

    # Parking area
    area_name = "N/A"
    if booking.slot and booking.slot.area:
        area_name = booking.slot.area.name

    # QR information
    qr_data = (
        "SMART PARKING SYSTEM\n"
        f"Booking ID: {booking.id}\n"
        f"Parking: {area_name}\n"
        f"Slot: {slot_number}\n"
        f"Date: {booking.booking_date}\n"
        f"Amount: ₹{booking.total_amount}\n"
        f"Status: {booking.status}"
    )

    # Create QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create image
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Save image to memory
    img = io.BytesIO()
    qr_image.save(img, format="PNG")
    img.seek(0)

    # Send PNG to browser
    return send_file(
        img,
        mimetype="image/png",
        as_attachment=False
    )
# ==========================================================
# PAYMENT PAGE
# ==========================================================

@user_bp.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    """
    Payment page for pending booking.

    College project version:
    Payment is simulated.
    No real money is transferred.
    """

    # ======================================================
    # GET PENDING BOOKING FROM SESSION
    # ======================================================

    pending = session.get(
        'pending_booking'
    )

    if not pending:
        flash(
            'No pending booking found.',
            'danger'
        )

        return redirect(
            url_for('user.parking_list')
        )

    # ======================================================
    # GET AREA
    # ======================================================

    area = ParkingArea.query.get(
        pending['area_id']
    )

    if not area:
        session.pop(
            'pending_booking',
            None
        )

        flash(
            'Parking location not found.',
            'danger'
        )

        return redirect(
            url_for('user.parking_list')
        )

    # ======================================================
    # GET SLOT
    # ======================================================

    slot = ParkingSlot.query.get(
        pending['slot_id']
    )

    if not slot:
        session.pop(
            'pending_booking',
            None
        )

        flash(
            'Parking slot not found.',
            'danger'
        )

        return redirect(
            url_for(
                'user.parking_details',
                area_id=area.id
            )
        )

    # ======================================================
    # POST — PAYMENT
    # ======================================================

    if request.method == 'POST':

        payment_method = request.form.get(
            'payment_method',
            'upi'
        )

        # Allowed payment methods
        allowed_methods = [
            'upi',
            'card',
            'netbanking',
            'wallet',
            'cash'
        ]

        if payment_method not in allowed_methods:
            flash(
                'Invalid payment method.',
                'danger'
            )

            return redirect(
                url_for('user.payment')
            )

        # ==================================================
        # RE-CHECK SLOT AVAILABILITY
        # ==================================================

        slot = ParkingSlot.query.get(
            pending['slot_id']
        )

        if not slot:
            flash(
                'Parking slot not found.',
                'danger'
            )

            return redirect(
                url_for('user.parking_list')
            )

        if slot.status != 'available':
            session.pop(
                'pending_booking',
                None
            )

            flash(
                'Sorry! This slot was booked by someone else.',
                'danger'
            )

            return redirect(
                url_for(
                    'user.parking_details',
                    area_id=area.id
                )
            )

        # ==================================================
        # DEMO PAYMENT
        # ==================================================

        # Generate demo transaction ID
        transaction_id = (
            'SP' +
            uuid.uuid4().hex[:10].upper()
        )

        # ==================================================
        # CREATE BOOKING
        # ==================================================

        booking = Booking(
            user_id=current_user.id,

            area_id=pending['area_id'],

            slot_id=pending['slot_id'],

            vehicle_id=pending.get(
                'vehicle_id'
            ),

            booking_date=pending['booking_date'],

            start_time=pending['start_time'],

            end_time=pending['end_time'],

            duration=pending['duration'],

            total_amount=pending['total_amount'],

            status='confirmed',

            booking_ref=generate_booking_ref(),

            notes=pending.get(
                'notes',
                ''
            )
        )

        db.session.add(
            booking
        )

        # ==================================================
        # CREATE PAYMENT
        # ==================================================

        payment_record = Payment(
            booking=booking,

            user_id=current_user.id,

            amount=pending['total_amount'],

            payment_method=payment_method,

            payment_status='completed',

            transaction_id=transaction_id
        )

        db.session.add(
            payment_record
        )

        # ==================================================
        # OCCUPY PARKING SLOT
        # ==================================================

        slot.status = 'occupied'

        # ==================================================
        # UPDATE AVAILABLE SLOTS
        # ==================================================

        area.available_slots = max(
            0,
            area.available_slots - 1
        )

        # ==================================================
        # SAVE DATABASE
        # ==================================================

        try:

            db.session.commit()

        except Exception as e:

            db.session.rollback()

            print(
                'PAYMENT ERROR:',
                e
            )

            flash(
                'Payment failed. Please try again.',
                'danger'
            )

            return redirect(
                url_for('user.payment')
            )

        # ==================================================
        # REMOVE TEMPORARY SESSION DATA
        # ==================================================

        session.pop(
            'pending_booking',
            None
        )

        # ==================================================
        # SUCCESS MESSAGE
        # ==================================================

        flash(
            'Payment successful! Booking confirmed.',
            'success'
        )

        return redirect(
            url_for(
                'user.parking_pass',
                booking_id=booking.id
            )
        )
    # ======================================================
    # GET — SHOW PAYMENT PAGE
    # ======================================================

    return render_template(
        'user/payment.html',
        area=area,
        slot=slot,
        pending=pending
    )
# ==========================================================
# DIGITAL PARKING PASS
# ==========================================================

@user_bp.route('/parking-pass/<int:booking_id>')
@login_required
def parking_pass(booking_id):

    booking = Booking.query.filter_by(
        id=booking_id,
        user_id=current_user.id
    ).first_or_404()

    area = ParkingArea.query.get(
        booking.area_id
    )

    slot = ParkingSlot.query.get(
        booking.slot_id
    )

    vehicle = None

    if booking.vehicle_id:
        vehicle = Vehicle.query.filter_by(
            id=booking.vehicle_id,
            user_id=current_user.id
        ).first()

    return render_template(
        'user/parking_pass.html',
        booking=booking,
        area=area,
        slot=slot,
        vehicle=vehicle
    )

@user_bp.route('/vehicles/delete/<int:vehicle_id>', methods=['POST'])
@login_required
def delete_vehicle(vehicle_id):

    vehicle = Vehicle.query.filter_by(
        id=vehicle_id,
        user_id=current_user.id
    ).first_or_404()

    if vehicle.bookings:
        flash(
            'This vehicle cannot be deleted because it has booking history.',
            'warning'
        )
        return redirect(url_for('user.vehicles'))

    db.session.delete(vehicle)
    db.session.commit()

    flash('Vehicle deleted successfully.', 'success')

    return redirect(url_for('user.vehicles'))

@user_bp.route('/vehicles/add', methods=['GET', 'POST'])
@login_required
def add_vehicle():

    if request.method == 'POST':

        vehicle_number = request.form.get('vehicle_number', '').strip().upper()
        vehicle_type = request.form.get('vehicle_type', 'car')
        color = request.form.get('color', '').strip()
        brand = request.form.get('brand', '').strip()

        if not vehicle_number:
            flash('Please enter vehicle number.', 'danger')
            return redirect(url_for('user.add_vehicle'))

        allowed_types = [
            'car',
            'bike',
            'suv',
            'truck',
            'ev'
        ]

        if vehicle_type not in allowed_types:
            flash('Invalid vehicle type.', 'danger')
            return redirect(url_for('user.add_vehicle'))

        existing = Vehicle.query.filter_by(
            user_id=current_user.id,
            vehicle_number=vehicle_number
        ).first()

        if existing:
            flash('This vehicle is already added.', 'warning')
            return redirect(url_for('user.vehicles'))

        vehicle_count = Vehicle.query.filter_by(
            user_id=current_user.id
        ).count()

        vehicle = Vehicle(
            user_id=current_user.id,
            vehicle_number=vehicle_number,
            vehicle_type=vehicle_type,
            color=color,
            brand=brand,
            is_default=1 if vehicle_count == 0 else 0
        )

        db.session.add(vehicle)
        db.session.commit()

        flash('Vehicle added successfully.', 'success')

        return redirect(url_for('user.vehicles'))

    # ⭐ VERY IMPORTANT
    # This opens the Add Vehicle page
    return render_template('user/add_vehicle.html')