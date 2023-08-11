from flask import session, redirect, url_for
from functools import wraps
from ..database.admin_table import get_admin
from ..database.notification_table import get_notification
from .helpers import filter_func


# RESTRICTS ACCESS TO AUTH PAGES IF ALREADY AUTHORIZED
def guest_only(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "logged_in" in session and session["admin"]:
            return redirect('/dashboard')
        return view_func(*args, **kwargs)
    return wrapper


# RESTRICTS ACCESS TO ADMIN PAGES UNLESS AUTHORIZED
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "logged_in" in session and session.get("admin"):  # CHECK FOR LOGIN SESSION
            # GET NOTIFICATION
            notifications = get_notification(session.get('admin')['admin_id'])
            notifications = get_notification(session.get('admin')['admin_id'])
            session['unread_notifications'] = filter_func(notifications, lambda item, *rest: item.get('is_seen') == 0)
            session['read_notifications'] = filter_func(notifications, lambda item, *rest: item.get('is_seen') == 1)

            return view_func(*args, **kwargs)
        return redirect('/')
    return wrapper


# ENSURE ONE ADMIN IS REGISTERED 
def ensure_only_one_admin(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # CHECK IF ADMIN ALREADY EXISTS
        admin = get_admin()
        if admin:  
            return redirect("/")
        
        return view_func(*args, **kwargs)
    return wrapper
