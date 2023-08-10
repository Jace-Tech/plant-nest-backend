from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, current_app
from functools import wraps
import jwt
import uuid
import datetime
import bcrypt
from ..utils.admin_manager import admin_manager
from ..database import get_connection
from app import create_app

auth = Blueprint("auth", __name__)
app = current_app

connection, cursor = get_connection()


@auth.get("/")
def login_page():
    return render_template("signin.html")


@auth.post("/")
def handle_login_page():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    sql = "SELECT * FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return jsonify({"message": "Invalid email or password"}), 401

    # Generate JWT token
    secret_key = str(app.config["APP_SECRET"])
    payload = {"user_id": user["user_id"], "username": user["username"]}
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return jsonify({"message": "Login successful", "token": token}), 200


# Handle the user signup route
@auth.post("/signup")
def signup_page():
    data = request.get_json()
    fullname = data.get("fullName")
    username = data.get("username")
    contact_number = data.get("contactNumber")
    email = data.get("email")
    password = data.get("password")

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user_username = cursor.fetchone()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_email = cursor.fetchone()
    cursor.close()

    if user_email:
        return jsonify({"message": "Email already exists"}), 400

    if user_username:
        return jsonify({"message": "Username already exists"}), 400

    user_id = str(uuid.uuid4())[:20]
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    sql = "INSERT INTO users (user_id, fullname, username, contact_number, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (user_id, fullname, username, contact_number, email, hashed_password))
    connection.commit()
    cursor.close()

    # Generate a JWT
    payload = {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}
    secret_key = str(app.config['SECRET_KEY'])
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return jsonify({"message": "User registered successfully", "token": token}), 201


# This decorator restricts access to admin pages unless authorized to do so
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "username" in session and admin_manager.is_admin(session["username"]):
            return view_func(*args, **kwargs)
        else:
            return redirect(url_for('admin_login_page'))

    return wrapper


# Handle admin login route
@auth.get("/admin/")
def admin_login_page():
    return render_template("admin/signin.html")