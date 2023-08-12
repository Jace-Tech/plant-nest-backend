from flask import Blueprint, render_template, flash, request, redirect
from ..utils.errors import CustomError
from ..utils.helpers import generate_id
from ..database.category_table import get_all_categories, get_category_by_id
from ..database import get_connection
from ..database.user_table import get_all_users
from ..utils.decorators import admin_required

customer = Blueprint("customer", __name__)


@customer.get("/")
@admin_required
def view_customer_page():
    all_customers = None
    try:
        db = get_connection()
        if not db:
            raise CustomError("Failed to connect to database")
        all_customers = get_all_users()  # Use the function to fetch customers
    except CustomError as e:
        flash(e.message, category=e.category)
        print(e)
    except Exception as e:
        flash(str(e), category="error")
        print(e)
    finally:
        return render_template("customers.html", customers=all_customers)
