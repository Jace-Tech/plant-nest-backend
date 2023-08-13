from flask import Blueprint, request, render_template, current_app
from ..utils.errors import catch_exception, CustomRequestError
from ..utils.helpers import generate_id, response
from ..database import get_connection
from ..database.order_table import get_order_by_id, get_users_order
from ..database.user_table import get_one_user
from ..database.notification_table import create_notification
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from ..utils.variables import APP_LOGO
from ..utils.mailer import send_mail
import json
import datetime

orders = Blueprint("orders", __name__)

@orders.post("/create")
@catch_exception
# @jwt_required
def create_order_():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    user = get_one_user(user_id)
    if not user: raise CustomRequestError("No user found", 404)

    db = get_connection()
    if not db: raise CustomRequestError("Failed to connect to database", 500)
    conn, cursor = db

    # GET DATA
    data = request.get_json()
    order_id = generate_id("ORD")
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    address = data.get('address')
    email = data.get('email')
    phone = data.get('phone')
    products = json.dumps(data.get('products'))
    amount = data.get('amount')

    # ADD ORDER TO DATABASE
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO orders (order_id, user_id, firstname, lastname, phone, email, products, address, amount, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, [order_id, user_id, firstname, lastname, phone, email, products, address, amount, now])
    conn.commit()

    # NOTIFY ADMIN
    create_notification(f"Order request", "Customer with {user_id} requested for an order", "ADMIN")

    # SEND USER EMAIL
    message = render_template("email/order.html", 
        APP_LOGO=APP_LOGO,
        year=datetime.datetime.now().strftime("%Y"),
        order_id=order_id
    )
    send_mail(current_app, "Order Request⏱", [user.get('email')], message, True)

    if not cursor.rowcount: raise CustomRequestError("Failed create order", 500)

    # GET ORDER
    order = get_order_by_id(cursor.lastrowid)
    return response("Order created!", order)


# GET ORDER BY ID
@orders.get("/<id>")
@catch_exception
def handle_get_order(id):
    order = get_order_by_id(id)
    return response("Order", order)


# GET USERS ORDER
@orders.get("/user")
@catch_exception    
def handle_get_users_order():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    users_orders = get_users_order(user_id)
    return response("Users order", users_orders)



