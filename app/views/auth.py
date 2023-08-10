from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, current_app
from functools import wraps
import uuid
import bcrypt
from ..utils.admin_manager import admin_manager
from flask_jwt_extended import create_access_token
from ..database import get_connection
from ..utils.helpers import response
from ..utils.errors import CustomRequestError

auth = Blueprint("auth", __name__)
app = current_app

connection, cursor = get_connection()


@auth.get("/")
def login_page():
    return render_template("signin.html")


@auth.get("/signup")
def signup_page():
    return render_template("signup.html")


@auth.post('/signup')
def handle_admin_sign_page():
    data = request.form
    fullname = data.get("fullName")
    email = data.get("email")
    image = data.get("image")
    password = data.get("password")

    cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
    user_email = cursor.fetchone()

    if user_email:
        raise CustomRequestError("Email already exists", 400)

    # Insert the user into the database
    admin_id = str(uuid.uuid4())[:20]
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    sql = "INSERT INTO admins (admin_id, name, image, email, password) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (admin_id, fullname, image, email, hashed_password))
    connection.commit()

    # Login the user immediately
    sql = "SELECT admin_id FROM admins WHERE email = %s"
    cursor.execute(sql, (email,))
    admin = cursor.fetchone()
    token = create_access_token(identity=admin['user_id'])
    admin_manager.add_admin(admin['username', admin['password']])
    return redirect('login_page')