from flask import session, redirect, url_for
from functools import wraps
from ..database.admin_table import get_admin


# RESTRICTS ACCESS TO ADMIN PAGES UNLESS AUTHORIZED
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "logged_in" in session and session["admin"]:  # CHECK FOR LOGIN SESSION
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
