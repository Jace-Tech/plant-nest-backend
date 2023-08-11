from flask import Blueprint, render_template
from ..database.plant_table import get_all_plants

dashboard = Blueprint("dashboard", __name__)

# ALL ADMIN ROUTES
@dashboard.get("/dashboard")
def dashboard_page():
  plants = get_all_plants()
  return render_template('dashboard.html', plants=plants)

# AUTH ROUTES
from .auth  import auth
dashboard.register_blueprint(auth)

# PRODUCT ROUTES
from .plants import plants
dashboard.register_blueprint(plants, url_prefix="/plants")


