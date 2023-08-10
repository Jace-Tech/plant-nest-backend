from flask import Blueprint, render_template

product = Blueprint("product", __name__)

@product.get("/products")
# TODO: PREVENT UNAUTHORIZED ACCESS
def view_product_page():
  return render_template("products.html")