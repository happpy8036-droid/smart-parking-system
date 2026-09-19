"""Utility helpers for Smart Parking System"""
import random
import string
from datetime import datetime


def generate_booking_ref():
    """Generate a unique booking reference number"""
    timestamp = datetime.now().strftime('%y%m%d')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"SP-{timestamp}-{random_str}"


def format_currency(amount):
    """Format amount as Indian currency"""
    return f"₹{amount:,.2f}"


def get_hours_between(start_time, end_time):
    """Calculate hours between two time strings"""
    try:
        fmt = '%H:%M'
        start = datetime.strptime(start_time, fmt)
        end = datetime.strptime(end_time, fmt)
        diff = (end - start).total_seconds() / 3600
        return max(1, round(diff))
    except (ValueError, TypeError):
        return 1
