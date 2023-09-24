from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps
from ..database import get_connection
from ..database.user_table import get_one_user
from ..utils.helpers import dict_except, response
from ..utils.errors import CustomRequestError, catch_exception
import bcrypt


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



@user.put('/change-password')
@catch_exception
@jwt_required()
def handle_change_password():
    current_user_id = get_jwt_identity()

    data = request.get_json()
    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")

    sql = "SELECT password FROM users WHERE user_id = %s"
    cursor.execute(sql, (current_user_id,))
    user = cursor.fetchone()

    if not user or not bcrypt.checkpw(old_password.encode("utf-8"), user["password"].encode("utf-8")):
        return jsonify({"message": "Invalid old password"}), 401

    # Hash the new password
    hashed_new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

    cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (hashed_new_password, current_user_id))
    connection.commit()
    cursor.close()

    return response("Password changed successfully")


@user.post('/reset-password')
@catch_exception
def handle_reset_password():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    cpassword = data.get("passwordConfirm")

    # Retrieve the user from the database
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user: raise CustomRequestError("User not found", 404)
    if password != cpassword: raise CustomRequestError("Passwords do not match", 400)

    # Hash the new password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Update the user's password in the database
    sql = "UPDATE users SET password = %s WHERE email = %s"
    cursor.execute(sql, (hashed_password, email))
    connection.commit()
    cursor.close()

    return response("Password reset successful")
