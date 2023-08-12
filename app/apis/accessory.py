from flask import Blueprint
from ..database import get_connection
from ..utils.helpers import response
from ..utils.errors import catch_exception
from ..database.accessory_table import get_all_accessories, get_one_accessory

accessories = Blueprint("accessories", __name__)
connection, cursor = get_connection()


@accessories.get('/')
@catch_exception
def get_accessories():
    # QUERY THE DATABASE FOR ALL THE PLANTS
    accessories = get_all_accessories()
    return response("All accessories", accessories)


@accessories.get('/<accessory_id>')
@catch_exception
def get_one_accessories(accessory_id):
    accessory = get_one_accessory(accessory_id)
    return response("Accessory", accessory)