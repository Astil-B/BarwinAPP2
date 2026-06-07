from datetime import datetime

from flask import flash

DT_FORMAT = "%d-%m-%Y %H:%M"
DT_ERROR = "Date must be in DD-MM-YYYY HH:MM format, e.g. 25-12-2025 20:00"


def flash_errors(form):
    for field, errors in form.errors.items():
        label = getattr(getattr(form, field), "label", None)
        name = label.text if label else field
        for error in errors:
            flash(f"{name}: {error}", "error")


def parse_dt(value):
    """takes DD-MM-YYYY HH:MM string, returning (datetime, none)"""
    try:
        return datetime.strptime((value or "").strip(), DT_FORMAT), None
    except ValueError:
        return None, DT_ERROR
