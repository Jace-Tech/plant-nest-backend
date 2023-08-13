from flask import Blueprint, request, jsonify, render_template, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps
from ..database import get_connection
from ..database.user_table import get_one_user
from ..database.order_table import get_order_by_id, get_users_order
from ..database.notification_table import create_notification
from ..utils.helpers import dict_except, response, generate_id
from ..utils.mailer import send_mail
from ..utils.errors import CustomRequestError, catch_exception
import bcrypt
from ..utils.variables import APP_LOGO
import json
import datetime


user = Blueprint("user", __name__)
connection, cursor = get_connection()


# decorator to check if the user is logged in
def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            user_id = get_jwt_identity()  # Get the user's ID from the JWT token
            if user_id is None:
                return jsonify({"message": "Unauthorized"}), 401
            return view_func(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": "Unauthorized"}), 401

    return wrapper


# GET USER ROUTE
@user.get('/<id>')
@catch_exception
def user_profile(id):
    user = get_one_user(id)
    if not user: raise CustomRequestError("User not found", 404)
    data = dict_except(user, "password")
    return response("User details", data)


# UPDATE PROFILE ROUTE
@user.route('/update-profile', methods=['PUT', 'PATCH'])
@catch_exception
@jwt_required()
def edit_profile():
    current_user_id = get_jwt_identity()
    prevData = get_one_user(current_user_id)

    # CHECK IF USER EXISTS
    if not prevData: raise CustomRequestError("No user found", 404)

    data = request.get_json()
    fullname = data.get("fullName") or prevData['fullname']
    email = data.get("email") or prevData['email']
    username = data.get("username") or prevData['username']
    contact_number = data.get("contactNumber") or prevData['contact_number']

    sql = """
        UPDATE users 
        SET fullname = %s, contact_number = %s, username = %s, email = %s
        WHERE user_id = %s
    """
    cursor.execute(sql, (fullname, contact_number, username, email, current_user_id))
    connection.commit()

    # GET NEW UPDATE
    user =  get_one_user(current_user_id)
    data = dict_except(user, "password")
    cursor.close()

    return response("Profile updated successfully", data)


# RESET PASSWORD ROUTE
# @user.get('/reset-password')
# @catch_exception
# def initiate_password_reset():
#     email = request.get_json().get('email')
#     if not email: raise CustomRequestError("Please enter your email address", 400)

#     # SEND EMAIL FOR EMAIL VERIFICATION
    