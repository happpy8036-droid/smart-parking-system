"""Payment Routes — Payment processing"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.booking import Booking
from models.payment import Payment
from extensions import db
from datetime import datetime

payment_bp = Blueprint('payment', __name__)


@payment_bp.route('/process/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def process(booking_id):
    """Process payment for a booking"""
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('user.booking_history'))

    if request.method == 'POST':
        method = request.form.get('method', 'upi')

        payment = Payment(
            booking_id=booking.id,
            user_id=current_user.id,
            amount=booking.total_amount,
            payment_method=method,
            payment_status='completed'
        )
        db.session.add(payment)
        booking.status = 'confirmed'
        db.session.commit()
        flash('Payment successful!', 'success')
        return redirect(url_for('user.booking_details', booking_id=booking.id))

    return render_template('user/payment.html', booking=booking)


@payment_bp.route('/status/<int:booking_id>')
@login_required
def status(booking_id):
    """Check payment status"""
    from flask import jsonify
    booking = Booking.query.get_or_404(booking_id)
    payment = Payment.query.filter_by(booking_id=booking_id).first()
    return jsonify({
        'booking_id': booking_id,
        'status': booking.status,
        'payment': {
            'method': payment.payment_method if payment else None,
            'status': payment.payment_status if payment else None,
            'amount': payment.amount if payment else None
        }
    })
