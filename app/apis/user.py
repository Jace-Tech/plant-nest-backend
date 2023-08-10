from flask import Blueprint, redirect, request, url_for, jsonify, session
from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps
from app.database import get_connection
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


@user.get('/user')
def user_profile():
    pass


@user.put('/update-profile')
@jwt_required()
def edit_profile():
    current_user_id = get_jwt_identity()
    print(current_user_id)

    data = request.get_json()
    new_fullname = data.get("fullname")
    new_contact_number = data.get("contactNumber")

    print(new_fullname)
    print(new_contact_number)
    sql = "UPDATE users SET fullname = %s, contact_number = %s WHERE user_id = %s"
    cursor.execute(sql, (new_fullname, new_contact_number, current_user_id))
    connection.commit()
    cursor.close()
    print("Committed")

    return jsonify({"message": "Profile updated successfully"}), 200


@user.get('/change-password')
def change_password():
    pass


@user.put('/change-password')
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

    return jsonify({"message": "Password changed successfully"}), 200