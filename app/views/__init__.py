from flask import Blueprint, render_template, request, redirect, flash
from ..database.plant_table import get_all_plants
from ..database import get_connection
from ..utils.decorators import admin_required
from ..utils.errors import CustomError

dashboard = Blueprint("dashboard", __name__)

# ALL ADMIN ROUTES
@dashboard.get("/dashboard")
@admin_required
def dashboard_page():
    plants = get_all_plants()
    return render_template('dashboard.html', plants=plants)


@dashboard.get("/notification/<id>")
@admin_required
def mark_notification_read(id):
    try:
        db = get_connection()
        if not db: raise CustomError("Can't connect to database")

        conn, cursor = db
        sql = "UPDATE notifications SET is_seen = 1 WHERE notification_id = %s"
        cursor.execute(sql, [id])
        conn.commit()

        flash("Notification updated", "success")
    except CustomError as e:
        flash(e.message, e.category)
        
    return redirect("/dashboard")
        

# AUTH ROUTES
from .auth  import auth
dashboard.register_blueprint(auth)

# PLANT ROUTES
from .plants import plants
dashboard.register_blueprint(plants, url_prefix="/plants")

# ACCESSORY ROUTES
from .accessory import accessory
dashboard.register_blueprint(accessory, url_prefix="/accessories")

# CATEGORY ROUTES
from .category import category
dashboard.register_blueprint(category, url_prefix="/categories")


