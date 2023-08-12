from flask import Blueprint, render_template, flash, request, redirect, url_for
import json
from ..database import get_connection
from ..database.accessory_table import get_all_accessories
from ..utils.errors import CustomError
from ..utils.helpers import generate_id
from ..utils.uploader import upload_file
from ..utils.decorators import admin_required
from datetime import datetime


accessory = Blueprint("accessory", __name__)


@accessory.get("/")
@admin_required
def view_accessory_page():
    accessories = None
    try:
        db = get_connection()
        if not db: raise CustomError("Failed to connect to database")
        accessories = get_all_accessories()
    except CustomError as e: 
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    finally:
        return render_template("accessory.html", accessories=accessories)


@accessory.get("/create")
@admin_required
def view_accessory_create_page():
    return render_template("accessory-create.html")


@accessory.post("/create")
@admin_required
def handle_accessory_create():
    try:
        data = request.form

        accessory_id = generate_id("acs_")
        accessory_name = data.get('name')
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
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO accessories (accessory_id, name, description, price, quantity, image_url, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (accessory_id, accessory_name, description, price, quantity, image_urls, now))
        conn.commit()

        if not cursor.rowcount: raise CustomError("Failed to create accessory")

        flash("Accessory created!", "success")
        return redirect(url_for('dashboard.accessory.view_accessory_page'))

    except CustomError as e: 
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    return render_template("accessory-create.html")


@accessory.get("/delete/<id>")
@admin_required
def handle_accessory_delete(id):
    try:
        # CHECK CONNECTION
        db = get_connection()
        if not db: raise CustomError("Couldn't connect to database", "error")

        conn, cursor = db
        sql = "DELETE FROM accessories WHERE accessory_id = %s"
        cursor.execute(sql, [id])
        conn.commit()
        conn.close()

        if not cursor.rowcount: raise CustomError("Failed to delete accessory", "error")
        flash("Accessory deleted successfully", "success")
        conn.close()
    except CustomError as e:
        flash(e.message, e.category)
    return redirect("/accessory")



@accessory.get("/edit/<id>")
@admin_required
def handle_accessory_edit(id):
    accessory = []
    try:
        # CHECK CONNECTION
        db = get_connection()
        if not db: raise CustomError("Couldn't connect to database", "error")

        conn, cursor = db
        sql = "SELECT * FROM accessories WHERE accessory_id = %s"
        cursor.execute(sql, [id])

        if not cursor.rowcount: raise CustomError("Plant not found", "error")
        accessory = cursor.fetchone()
        conn.close()
    except CustomError as e:
        flash(e.message, e.category)
    return render_template("edit-accessory.html", accessory=accessory)


@accessory.post("/update/<id>")
@admin_required
def handle_accessory_update(id):
    accessory = []
    try:
        # CHECK CONNECTION
        db = get_connection()
        if not db: raise CustomError("Couldn't connect to database", "error")
        conn, cursor = db

        # GET PLANT DETAILS
        data = request.form
        accessory_name = data.get('name')
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

        sql = """UPDATE accessories
            SET name = %s, description = %s, price = %s, quantity = %s, image_url = %s
            WHERE accessory_id = %s"""
        cursor.execute(sql, [accessory_name, description, price, quantity, image_urls, id])
        conn.commit()
        conn.close()

        if not cursor.rowcount: raise CustomError("Failed to update accessory", "error")
        flash("Accessory updated", "success")
        return redirect("/accessory")
    
    except CustomError as e:
        flash(e.message, e.category)

    except Exception as e:
        flash(str(e), "error")

    return render_template("edit-accessory.html", accessory=accessory)
