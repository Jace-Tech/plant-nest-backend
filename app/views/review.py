from flask import Blueprint, render_template, flash, request, redirect, url_for
from ..database import get_connection
from ..database.general_functions import select_product
from ..database.reviews_table import get_all_reviews,calculate_average_rating,fetch_products_with_average_ratings
from ..utils.errors import CustomError
from ..utils.decorators import admin_required


admin_review = Blueprint("admin_review", __name__)





@admin_review.get('/')
@admin_required
def view_all_reviews():
    all_reviews = None
    try:
        all_reviews = get_all_reviews()
    except Exception as e:
        flash(str(e), category="error")

    finally:
        return render_template("reviews.html", reviews=all_reviews)
    
@admin_review.get('/ratings')
@admin_required
def get_products_with_average_ratings_route():
    
    products_with_ratings = []  
 
    
 
    try:
        
        products_with_ratings = fetch_products_with_average_ratings()
        print("products_with_ratings")
        
       
      
    except Exception as e:
        flash(str("check"), category="error")
        
    finally:
        return render_template("productRatings.html", products_with_ratings=products_with_ratings)




@admin_review.get('/product/<product_id>')
@admin_required
def view_product_details(product_id):
    product_details = []
    
    
    
    try:
        product_details = select_product(product_id)
    
        
        average_rating = calculate_average_rating(product_id)

        return render_template("product_details.html", product=product_details, average_rating=average_rating)

    except Exception as e:
        flash(str(e), category="error")
        return redirect(url_for("view_all_reviews"))