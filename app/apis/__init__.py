from flask import Blueprint
from ..utils.helpers import response
from ..utils.variables import APP_NAME
from .user import user

api = Blueprint("apis", __name__)

# DEFAULT API ROUTE
@api.get("/")
def default_api():
  return response(f"{APP_NAME} API is running")

api.register_blueprint(user, url_prefix="/user")