from flask import Blueprint, request
from ..database import get_connection
from ..utils.helpers import response, map_func
from ..utils.errors import catch_exception, CustomRequestError
from ..database.plant_table import get_all_plants, get_one_plant

plants = Blueprint("plants", __name__)

connection, cursor = get_connection()


@plants.get('/')
@catch_exception
def get_plants():
    # QUERY THE DATABASE FOR ALL THE PLANTS
    plants = get_all_plants()
    return response("All plants", plants)


@plants.get('/<plant_id>')
@catch_exception
def get_one_plants():
    plant = get_one_plant()
    return response("Plant", plant)