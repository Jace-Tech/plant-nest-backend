from flask import Blueprint, render_template, flash, request, redirect
from ..utils.errors import CustomError
from ..utils.helpers import generate_id
from ..database.category_table import get_all_categories, get_category_by_id
from ..database import get_connection
from ..utils.decorators import admin_required
from datetime import datetime


category = Blueprint("category", __name__)

@category.get("/")
@admin_required
def view_category_page():
    categories = []
    editing = None
    try:
        id = request.args.get('edit_id')
        if id:
            editing = get_category_by_id(id)
        categories = get_all_categories()
    except CustomError as e:
        flash(e.message, e.category)

    except Exception as e:
        flash(str(e), "error")

    return render_template("category.html", categories=categories, editing=editing)




# CREATE
@category.post("/create")
@admin_required
def handle_create_category():
    try:
        db = get_connection()
        if not db: raise CustomError("Couldn't connect to database", "error")
        conn, cursor = db

        # GET FORM VALUES
        id = generate_id("cat_")
        category = request.form.get('category')

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO categories (category_id, name, date) VALUES (%s, %s, %s)"
        cursor.execute(sql, [id, category, now])
        conn.commit()
        
        if not cursor.rowcount: raise CustomError("Failed to update category")
        flash("Category added!", "success")

    except CustomError as e:
        flash(e.message, e.category)

    except Exception as e:
        flash(str(e), "error")

    return redirect("/categories/")



# UPDATE 
@category.post("/update/<id>")
@admin_required
def handle_update_category(id):
    try:
        db = get_connection()
        if not db: raise CustomError("Couldn't connect to database", "error")
        conn, cursor = db

        # GET FORM VALUES
        category = request.form.get('category')

        sql = "UPDATE categories SET name = %s WHERE category_id = %s"
        cursor.execute(sql, [category, id])
        conn.commit()
        
        if not cursor.rowcount: raise CustomError("Failed to update category")
        flash("Category updated successfully", "success")

    except CustomError as e:
        flash(e.message, e.category)

    except Exception as e:
        flash(str(e), "error")

    return redirect("/categories/")


# DELETE
@category.get("/delete/<id>")
@admin_required
def handle_delete_category(id):
    try:
        db = get_connection()
        if not db: raise CustomError("Couldn't connect to database", "error")
        conn, cursor = db

        sql = "DELETE FROM categories WHERE category_id = %s"
        cursor.execute(sql, [id])
        conn.commit()

        if not cursor.rowcount: raise CustomError("Failed to delete category")
        flash("Category deleted successfully", "success")

    except CustomError as e:
        flash(e.message, e.category)

    except Exception as e:
        flash(str(e), "error")

    return redirect("/categories/")