from flask import Blueprint, render_template, flash, request, redirect, url_for
import json
import csv
from ..database import get_connection
from ..database.plant_table import get_all_plants
from ..database.category_table import get_all_categories
from ..utils.errors import CustomError
from ..utils.helpers import generate_id
from ..utils.uploader import upload_file
from ..utils.decorators import admin_required

plants = Blueprint("plants", __name__)


@plants.get("/")
@admin_required
def view_plant_page():
    all_plants = None
    try:
        db = get_connection()
        if not db:
            raise CustomError("Failed to connect to database")
        all_plants = get_all_plants()
    except CustomError as e:
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    finally:
        return render_template("plants.html", plants=all_plants)


@plants.get("/create")
@admin_required
def view_plant_create_page():
    all_categories = None

    try:
        db = get_connection()
        if not db:
            raise CustomError("Failed to connect to database")
        all_categories = get_all_categories()

    except CustomError as e:
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    finally:
        return render_template("plant-create.html", categories=all_categories)


@plants.post("/create")
@admin_required
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
        if not db:
            raise CustomError("Failed to connect to database")
        conn, cursor = db

        # STORE IN DB
        query = "INSERT INTO plants (plant_id, name, description, price, quantity, image_url, category_id, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (plant_id, plant_name, description,
                       price, quantity, image_urls, category, 'now()'))
        conn.commit()

        if not cursor.rowcount:
            raise CustomError("Failed to create plant")

        flash("Plant created!", "success")
        return redirect(url_for('dashboard.plants.view_plant_page'))

    except CustomError as e:
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    all_categories = get_all_categories()
    return render_template("plant-create.html", categories=all_categories)


@plants.get("/delete/<id>")
@admin_required
def handle_plant_delete(id):
    try:
        # CHECK CONNECTION
        db = get_connection()
        if not db:
            raise CustomError("Couldn't connect to database", "error")

        conn, cursor = db
        sql = "DELETE FROM plants WHERE plant_id = %s"
        cursor.execute(sql, [id])
        conn.commit()
        conn.close()

        if not cursor.rowcount:
            raise CustomError("Failed to delete plant", "error")
        flash("Plant deleted successfully", "success")
        conn.close()
    except CustomError as e:
        flash(e.message, e.category)
    return redirect("/plants")


@plants.get("/edit/<id>")
@admin_required
def handle_plant_edit(id):
    plant = []
    categories = []
    try:
        # CHECK CONNECTION
        db = get_connection()
        if not db:
            raise CustomError("Couldn't connect to database", "error")
        categories = get_all_categories()

        conn, cursor = db
        sql = "SELECT * FROM plants WHERE plant_id = %s"
        cursor.execute(sql, [id])

        if not cursor.rowcount:
            raise CustomError("Plant not found", "error")
        plant = cursor.fetchone()
        conn.close()
    except CustomError as e:
        flash(e.message, e.category)
    return render_template("edit-plant.html", plant=plant, categories=categories)


@plants.post("/update/<id>")
@admin_required
def handle_plant_update(id):
    plant = []
    try:
        # CHECK CONNECTION
        db = get_connection()
        if not db:
            raise CustomError("Couldn't connect to database", "error")
        conn, cursor = db

        # GET PLANT DETAILS
        data = request.form
        plant_name = data.get('name')
        category = data.get('category')
        quantity = data.get('quantity')
        price = data.get('price')
        description = data.get('description')
        image_urls = data.get('image_urls')

        files = request.files.getlist("images")
        if files[0].filename != "":
            # IF THERE'S NEW UPLOAD, CLEAR THE PREV ONES
            image_urls = []
            for file in files:
                print("FILE:", file)
                pub_id = generate_id()
                result = upload_file(file, pub_id)
                image_urls.append(result.get('secure_url'))
            image_urls = json.dumps(image_urls)

        sql = """UPDATE plants 
            SET name = %s, description = %s, price = %s, quantity = %s, image_url = %s, category_id = %s
            WHERE plant_id = %s"""
        cursor.execute(sql, [plant_name, description, price,
                       quantity, image_urls, category, id])
        conn.commit()
        conn.close()

        if not cursor.rowcount:
            raise CustomError("Failed to update plant", "error")
        flash("Plant updated", "success")
        return redirect("/plants")

    except CustomError as e:
        flash(e.message, e.category)

    except Exception as e:
        flash(str(e), "error")

    return render_template("edit-plant.html", plant=plant)


@plants.post("/plants/create/bulk")
def handle_create_bluk():
    try:
        # GET UPLOADED FILES
        file = request.files.get("file")
        if not file.filename:
            raise CustomError("File not found")
        data = []

        reader = csv.reader(file)
        for row in reader:
            data.append(row)

        return data
    except Exception as e:
        # flash(str(e), "error")
        return {'success': True}
