from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def manager_required(view):

    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in.", "error")
            return redirect(url_for("Login.login"))
        if current_user.role != "manager":
            flash("Managers only — you do not have permission for that.", "error")
            return redirect(url_for("Login.home"))
        return view(*args, **kwargs)

    return wrapper
