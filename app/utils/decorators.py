from flask import session, redirect, url_for
from functools import wraps


# This decorator restricts access to admin pages unless authorized to do so
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "admin" in session and session["admin"]:  # Assuming you store admin status in the session
            return view_func(*args, **kwargs)
        else:
            return redirect(url_for('login_page'))

    return wrapper
