from flask import Blueprint, request
from ..database import get_connection
from ..utils.helpers import response

plants = Blueprint("plants", __name__)

connection, cursor = get_connection()


@plants.get('/')
def get_all_plants():

    # QUERY THE DATABASE FOR ALL THE PLANTS
    sql = "SELECT * FROM plants"
    cursor.execute(sql)
    plants = cursor.fetchall()
    return response(plants)


@plants.get('/plants/<int:plant_id>')
def get_plant_by_id(plant_id):

    # QUERY THE DATABASE FOR THE PLANT WITH THE ID
    sql = "SELECT * FROM plants WHERE plant_id = %s"
    cursor.execute(sql, (plant_id,))
    plant = cursor.fetchone()
    return response(plant)