from flask import Blueprint, render_template, flash, request, redirect, url_for
import json
from ..database import get_connection
from ..database.plant_table import get_all_plants
from ..database.category_table import get_all_categories
from ..utils.errors import CustomError
from ..utils.helpers import generate_id
from ..utils.uploader import upload_file
from datetime import datetime

plants = Blueprint("plants", __name__)


@plants.get("/")
# TODO: PREVENT UNAUTHORIZED ACCESS
def view_plant_page():
    all_plants = None
    try:
        db = get_connection()
        if not db: raise CustomError("Failed to connect to database")
        all_plants = get_all_plants()
    except CustomError as e: 
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    finally:
        return render_template("plants.html", plants=all_plants)



@plants.get("/create")
# TODO: PREVENT UNAUTHORIZED ACCESS
def view_plant_create_page():
    all_categories = None

    try:
        db = get_connection()
        if not db: raise CustomError("Failed to connect to database")
        all_categories = get_all_categories()

    except CustomError as e: 
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    finally:
        return render_template("plant-create.html", categories=all_categories)



@plants.post("/create")
# TODO: PREVENT UNAUTHORIZED ACCESS
def handle_plant_create():
    try:
        data = request.form

        plant_id = generate_id("pln_")
        plant_name = data.get('name')
        category = data.get('category')
        quantity = data.get('quantity')
        price = data.get('price')
        description = data.get('description')
        image_urls = []

        # HANDLE IMAGES
        files = request.files.getlist("images")

        for file in files:
            print("FILE:", file)
            pub_id = generate_id()
            result = upload_file(file, pub_id)
            image_urls.append(result.get('secure_url'))

        # CONVERT TO JSON
        image_urls = json.dumps(image_urls)

        db = get_connection()
        if not db: raise CustomError("Failed to connect to database")
        conn, cursor = db

        # STORE IN DB
        query = "INSERT INTO plants (plant_id, name, description, price, quantity, image_url, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (plant_id, plant_name, description, price, quantity, image_urls, category))
        conn.commit() 

        if not cursor.rowcount: raise CustomError("Failed to create plant")

        flash("Plant created!", "success")
        return redirect(url_for('dashboard.plants.view_plant_page'))

    except CustomError as e: 
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    all_categories = get_all_categories()
    return render_template("plant-create.html", categories=all_categories)



