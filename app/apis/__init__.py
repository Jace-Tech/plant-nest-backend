from flask import Blueprint
from ..utils.helpers import response
from ..utils.variables import APP_NAME
from .user import user
from .cart import cart
from .wishlist import wishlist

api = Blueprint("apis", __name__)

# DEFAULT API ROUTE
@api.get("/")
def default_api():
    return response(f"{APP_NAME} API is running")

# TODO: REMEMBER TO MOVE THIS
api.register_blueprint(user, url_prefix="/user")
api.register_blueprint(cart, url_prefix="/cart")
api.register_blueprint(wishlist, url_prefix="/wishlist")