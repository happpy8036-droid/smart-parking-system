"""Home Routes — Landing Page"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from models.parking_area import ParkingArea
from models import Feedback
from extensions import db

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    """Landing page — show featured locations"""
    areas = ParkingArea.query.filter_by(is_active=1).order_by(ParkingArea.id).all()
    if current_user.is_authenticated:
        if current_user.__class__.__name__ == 'Admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.parking_list'))
    return render_template('home/index.html', areas=areas)
# ==============================
# ABOUT US
# ==============================

@home_bp.route('/about')
def about():
    return render_template('home/about.html')


# ==============================
# CONTACT US
# ==============================

@home_bp.route('/contact')
def contact():
    return render_template('home/contact.html')


# ==============================
# FEEDBACK
# ==============================

@home_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        comment = request.form.get('comment', '').strip()

        if not rating or rating < 1 or rating > 5:
            flash('Please select a rating between 1 and 5.', 'danger')
            return redirect(url_for('home.feedback'))

        if not comment:
            flash('Please enter your feedback.', 'danger')
            return redirect(url_for('home.feedback'))

        feedback = Feedback(
            user_id=current_user.id,
            rating=rating,
            comment=comment
        )

        db.session.add(feedback)
        db.session.commit()

        flash('Thank you! Your feedback has been submitted successfully.', 'success')
        return redirect(url_for('home.feedback'))

    return render_template('feedback.html')