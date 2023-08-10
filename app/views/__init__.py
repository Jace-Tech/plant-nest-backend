from flask import Blueprint, render_template

dashboard = Blueprint("dashboard", __name__)

# ALL ADMIN ROUTES
@dashboard.get("/dashboard")
def dashboard_page():
  return render_template('dashboard.html')

# AUTH ROUTES
from .auth  import auth
dashboard.register_blueprint(auth)

# PRODUCT ROUTES
from .plants import plants
dashboard.register_blueprint(plants, url_prefix="/plants")


