from flask import Blueprint, render_template

category = Blueprint("category", __name__)

@category.get("/")
def view_category_page():
    return render_template("category.html")