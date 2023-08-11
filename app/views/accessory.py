from flask import Blueprint, render_template

accessory = Blueprint("accessory", __name__)


@accessory.get("/")
def view_accessory_page():
  return render_template("accessory.html")


@accessory.get("/create")
def view_accessory_create_page():
  return render_template("accessory-create.html")