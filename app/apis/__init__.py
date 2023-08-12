from flask import Blueprint
from ..utils.helpers import response
from ..utils.variables import APP_NAME
from .user import user
from .cart import cart
from .auth import auth
from .plants import plants
from .orders import order_api
from .accessory import access
from .wishlist import wishlist

api = Blueprint("apis", __name__)

# DEFAULT API ROUTE
@api.get("/")
def default_api():
    return response(f"{APP_NAME} API is running")


api.register_blueprint(user, url_prefix="/user")
api.register_blueprint(auth, url_prefix="/auth")
api.register_blueprint(cart, url_prefix="/cart")
api.register_blueprint(wishlist, url_prefix="/wishlist")
api.register_blueprint(plants, url_prefix="/plants")
api.register_blueprint(access, url_prefix="/access")
api.register_blueprint(order_api, url_prefix="/order")