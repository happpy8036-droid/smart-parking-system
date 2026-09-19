"""Admin Routes — Dashboard, Users, Parking Management, Bookings, Reports"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Admin, User, Vehicle, ParkingArea, ParkingSlot, Booking, Payment, Notification, Feedback
from extensions import db
from datetime import datetime
from utils.decorators import admin_required
from functools import wraps

admin_bp = Blueprint('admin', __name__)


def admin_only(f):
    """Decorator to ensure only admins can access"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.__class__.__name__ != 'Admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        admin = Admin.query.filter_by(email=email, is_active=1).first()
        if admin and admin.check_password(password):
            from flask_login import login_user
            login_user(admin)
            flash('Welcome, Admin!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('admin/login.html')


@admin_bp.route('/dashboard')
@login_required
@admin_only
def dashboard():
    """Admin dashboard with statistics"""
    total_users = User.query.filter_by(is_active=1).count()
    total_areas = ParkingArea.query.filter_by(is_active=1).count()
    total_bookings = Booking.query.count()
    confirmed_bookings = Booking.query.filter_by(status='confirmed').count()
    total_revenue = db.session.query(db.func.sum(Booking.total_amount)).filter_by(status='confirmed').scalar() or 0
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', total_users=total_users, total_areas=total_areas,
                           total_bookings=total_bookings, confirmed_bookings=confirmed_bookings,
                           total_revenue=total_revenue, recent_bookings=recent_bookings)


@admin_bp.route('/users')
@login_required
@admin_only
def users():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    users_list = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/users.html', users=users_list)


@admin_bp.route('/parking-locations')
@login_required
@admin_only
def parking_locations():
    """List all parking areas"""
    areas = ParkingArea.query.order_by(ParkingArea.created_at.desc()).all()
    return render_template('admin/parking_locations.html', areas=areas)


@admin_bp.route('/add-parking', methods=['GET', 'POST'])
@login_required
@admin_only
def add_parking():
    """Add a new parking area"""
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        city = request.form.get('city')
        area_name = request.form.get('area')
        price = request.form.get('price_per_hour', 50)
        description = request.form.get('description')
        area = ParkingArea(name=name, address=address, city=city, area=area_name,
                          price_per_hour=float(price), description=description, is_active=1)
        db.session.add(area)
        db.session.commit()
        flash('Parking area added successfully.', 'success')
        return redirect(url_for('admin.parking_locations'))
    return render_template('admin/add_parking.html')


@admin_bp.route('/edit-parking/<int:area_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def edit_parking(area_id):
    """Edit a parking area"""
    area = ParkingArea.query.get_or_404(area_id)
    if request.method == 'POST':
        area.name = request.form.get('name', area.name)
        area.address = request.form.get('address', area.address)
        area.city = request.form.get('city', area.city)
        area.area = request.form.get('area', area.area)
        area.price_per_hour = float(request.form.get('price_per_hour', area.price_per_hour))
        area.description = request.form.get('description', area.description)
        db.session.commit()
        flash('Parking area updated.', 'success')
        return redirect(url_for('admin.parking_locations'))
    return render_template('admin/edit_parking.html', area=area)


@admin_bp.route('/parking-details/<int:area_id>')
@login_required
@admin_only
def parking_details(area_id):
    """View parking area details"""
    area = ParkingArea.query.get_or_404(area_id)
    slots = ParkingSlot.query.filter_by(area_id=area_id).all()
    return render_template('admin/parking_details.html', area=area, slots=slots)


@admin_bp.route('/parking-slots/<int:area_id>')
@login_required
@admin_only
def parking_slots(area_id):
    """Manage slots for a parking area"""
    slots = ParkingSlot.query.filter_by(area_id=area_id).all()
    area = ParkingArea.query.get(area_id)
    if not area:
        flash('Parking area not found.', 'danger')
        return redirect(url_for('admin.parking_locations'))
    return render_template('admin/parking_slots.html', area_id=area_id, area=area, slots=slots)


@admin_bp.route('/add-slot/<int:area_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def add_slot(area_id):
    """Add a new parking slot"""
    if request.method == 'POST':
        slot = ParkingSlot(
            area_id=area_id,
            slot_number=request.form.get('slot_number'),
            slot_type=request.form.get('slot_type', 'standard'),
            price_per_hour=float(request.form.get('price_per_hour', 50)),
            row=request.form.get('row'),
            col=int(request.form.get('col', 0)),
        )
        db.session.add(slot)
        db.session.commit()
        flash('Slot added.', 'success')
        return redirect(url_for('admin.parking_slots', area_id=area_id))
    return render_template('admin/add_slot.html', area_id=area_id)


@admin_bp.route('/edit-slot/<int:slot_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def edit_slot(slot_id):
    """Edit a parking slot"""
    slot = ParkingSlot.query.get_or_404(slot_id)
    if request.method == 'POST':
        slot.slot_number = request.form.get('slot_number', slot.slot_number)
        slot.slot_type = request.form.get('slot_type', slot.slot_type)
        slot.status = request.form.get('status', slot.status)
        slot.price_per_hour = float(request.form.get('price_per_hour', slot.price_per_hour))
        db.session.commit()
        flash('Slot updated.', 'success')
        return redirect(url_for('admin.parking_slots', area_id=slot.area_id))
    return render_template('admin/edit_slot.html', slot=slot)


@admin_bp.route('/delete-parking/<int:area_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def delete_parking(area_id):
    """Delete a parking area and all its slots/bookings"""
    area = ParkingArea.query.get_or_404(area_id)
    if request.method == 'POST':
        # Delete all bookings for this area first
        Booking.query.filter_by(area_id=area_id).delete(synchronize_session=False)
        # Delete all payments linked to those bookings
        # Delete all slots
        ParkingSlot.query.filter_by(area_id=area_id).delete(synchronize_session=False)
        # Delete the area
        db.session.delete(area)
        db.session.commit()
        flash(f'"{area.name}" deleted successfully.', 'success')
        return redirect(url_for('admin.parking_locations'))
    return render_template('admin/delete_parking.html', area=area)


@admin_bp.route('/delete-slot/<int:slot_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def delete_slot(slot_id):
    """Delete a parking slot"""
    slot = ParkingSlot.query.get_or_404(slot_id)
    area_id = slot.area_id
    if request.method == 'POST':
        db.session.delete(slot)
        db.session.commit()
        flash(f'Slot {slot.slot_number} deleted.', 'success')
        return redirect(url_for('admin.parking_slots', area_id=area_id))
    return render_template('admin/delete_slot.html', slot=slot, area_id=area_id)


@admin_bp.route('/bookings')
@login_required
@admin_only
def bookings():
    """View all bookings"""
    status_filter = request.args.get('status', '')
    query = Booking.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    bookings = query.order_by(Booking.created_at.desc()).all()
    return render_template('admin/bookings.html', bookings=bookings, status_filter=status_filter)


@admin_bp.route('/payments')
@login_required
@admin_only
def payments():
    """View all payments"""
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template('admin/payments.html', payments=payments)


@admin_bp.route('/reports')
@login_required
def reports():

    # Total bookings
    total_bookings = Booking.query.count()

    # Total users
    total_users = User.query.count()

    # Total parking locations
    total_locations = ParkingArea.query.count()

    # Location statistics
    location_stats = []

    locations = ParkingArea.query.all()

    for loc in locations:

        booking_count = (
            Booking.query
            .join(ParkingSlot, Booking.slot_id == ParkingSlot.id)
            .filter(ParkingSlot.area_id == loc.id)
            .count()
        )

        revenue = (
            db.session.query(
                db.func.coalesce(
                    db.func.sum(Booking.total_amount), 0
                )
            )
            .join(ParkingSlot, Booking.slot_id == ParkingSlot.id)
            .filter(ParkingSlot.area_id == loc.id)
            .scalar()
        )

        location_stats.append({
            'name': loc.name,
            'booking_count': booking_count,
            'revenue': revenue or 0
        })

    # Total revenue
    total_revenue = (
        db.session.query(
            db.func.coalesce(
                db.func.sum(Booking.total_amount), 0
            )
        ).scalar()
    )

    return render_template(
        'admin/reports.html',
        total_bookings=total_bookings,
        total_users=total_users,
        total_locations=total_locations,
        total_revenue=total_revenue or 0,
        location_stats=location_stats
    )


@admin_bp.route('/notifications')
@login_required
@admin_only
def notifications():
    """Admin notifications"""
    notifs = Notification.query.order_by(Notification.created_at.desc()).limit(50).all()
    return render_template('admin/notifications.html', notifications=notifs)


@admin_bp.route('/feedback')
@login_required
def feedback():

    feedbacks = Feedback.query.order_by(
        Feedback.created_at.desc()
    ).all()

    return render_template(
        'admin/feedback.html',
        feedbacks=feedbacks
    )


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_only
def settings():
    """Admin settings"""
    if request.method == 'POST':
        flash('Settings saved.', 'success')
    return render_template('admin/settings.html')

@admin_bp.route('/occupancy-heatmap')
@login_required
def occupancy_heatmap():
    """
    Parking occupancy heatmap.

    Shows parking occupancy percentage
    for each location and each hour.
    """

  
    selected_date = request.args.get(
        'date',
        datetime.now().strftime('%Y-%m-%d')
    )

   
    locations = ParkingArea.query.filter_by(
        is_active=1
    ).all()

    
    hours = list(range(6, 22))

    heatmap_data = []

    

    for location in locations:

        # Total slots in this location
        total_slots = ParkingSlot.query.filter_by(
            area_id=location.id
        ).count()

        # Avoid division by zero
        if total_slots == 0:
            total_slots = 1

        # Get bookings for this location/date
        bookings = Booking.query.filter(
            Booking.area_id == location.id,
            Booking.booking_date == selected_date,
            Booking.status.in_([
                'confirmed',
                'completed'
            ])
        ).all()

        hourly_data = []

        
        for hour in hours:

            hour_start = hour * 60
            hour_end = (hour + 1) * 60

            occupied = 0

            

            for booking in bookings:

                try:

                    start_parts = booking.start_time.split(':')
                    end_parts = booking.end_time.split(':')

                    booking_start = (
                        int(start_parts[0]) * 60
                        + int(start_parts[1])
                    )

                    booking_end = (
                        int(end_parts[0]) * 60
                        + int(end_parts[1])
                    )

                    # Handle overnight booking
                    if booking_end <= booking_start:
                        booking_end += 24 * 60

                    # Check overlap
                    if (
                        booking_start < hour_end
                        and booking_end > hour_start
                    ):
                        occupied += 1

                except Exception:
                    continue

           
            percentage = (
                occupied / total_slots
            ) * 100

            # Maximum 100%
            percentage = min(
                100,
                round(percentage)
            )


            if percentage < 30:
                level = 'low'

            elif percentage < 60:
                level = 'medium'

            elif percentage < 80:
                level = 'high'

            else:
                level = 'very-high'

            hourly_data.append({
                'hour': hour,
                'occupied': occupied,
                'total': total_slots,
                'percentage': percentage,
                'level': level
            })


        heatmap_data.append({
            'id': location.id,
            'name': location.name,
            'hourly': hourly_data
        })

    

    return render_template(
        'admin/occupancy_heatmap.html',
        heatmap_data=heatmap_data,
        hours=hours,
        selected_date=selected_date
    )