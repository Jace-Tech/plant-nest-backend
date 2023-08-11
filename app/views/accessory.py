from flask import Blueprint, render_template
from ..utils.decorators import admin_required

accessory = Blueprint("accessory", __name__)

@accessory.get("/")
@admin_required
def view_accessory_page():
    return render_template("accessory.html")

@accessory.get("/create")
@admin_required
def view_accessory_create_page():
	return render_template("accessory-create.html")