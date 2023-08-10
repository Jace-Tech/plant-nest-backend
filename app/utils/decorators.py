from flask import session, redirect, url_for
from functools import wraps
from ..utils.admin_manager import admin_manager


# This decorator restricts access to admin pages unless authorized to do so
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "username" in session and admin_manager.is_admin(session["username"]):
            return view_func(*args, **kwargs)
        else:
            return redirect(url_for('admin_login_page'))

    return wrapper
