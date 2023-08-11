from flask import Blueprint, render_template
from ..database.plant_table import get_all_plants
from ..utils.decorators import admin_required

dashboard = Blueprint("dashboard", __name__)

# ALL ADMIN ROUTES
@dashboard.get("/dashboard")
@admin_required
def dashboard_page():
    plants = get_all_plants()
    return render_template('dashboard.html', plants=plants)

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


