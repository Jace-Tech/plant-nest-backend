from flask import Blueprint, render_template, request, redirect, flash

from ..database.accessory_table import get_all_accessories
from ..database.order_table import get_all_orders, get_amount_for_period
from ..database.plant_table import get_all_plants
from ..database import get_connection
from ..database.user_table import get_all_users
from ..database.reviews_table import get_all_reviews

from ..utils.decorators import admin_required
from ..utils.errors import CustomError
from ..utils.helpers import map_func

import json

dashboard = Blueprint("dashboard", __name__)

# ALL ADMIN ROUTES
@dashboard.get("/dashboard")
@admin_required
def dashboard_page():
    users = get_all_users()
    accessories = get_all_accessories()
    orders = get_all_orders()
    reviews = get_all_reviews()
    plants = get_all_plants()

    daily = json.dumps(map_func(get_amount_for_period("daily"), lambda item, *_ : float(item['revenue'])))
    monthly = json.dumps(map_func(get_amount_for_period("monthly"), lambda item, *_ : float(item['revenue'])))


    return render_template('dashboard.html', 
        plants=plants,
        users=users,
        accessories=accessories,
        orders=orders,
        reviews=reviews,
        daily=daily,
        monthly=monthly
    )


# MARK NOTIFICATION AS READ
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

# CUSTOMER ROUTES
from .customers import customer
dashboard.register_blueprint(customer, url_prefix="/customers")