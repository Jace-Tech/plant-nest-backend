from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, current_app
import uuid
import bcrypt
from flask_jwt_extended import create_access_token
from ..database import get_connection
from ..utils.helpers import response
from ..utils.errors import CustomRequestError

auth = Blueprint("auth", __name__)
app = current_app

connection, cursor = get_connection()


@auth.post("/")
def login_page():
    data = request.form
    email = data.get("email")
    password = data.get("password")

    sql = "SELECT * FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()
    print(user)
    print("Check something")

    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        raise CustomRequestError("Invalid email or password", 400)

    # Generate JWT token
    token = create_access_token(identity=user["user_id"])

    return redirect('signup_page')


@auth.post('/signup')
def handle_signup_page():
    data = request.form
    fullname = data.get("fullName")
    username = data.get("username")
    contact_number = data.get("contactNumber")
    email = data.get("email")
    password = data.get("password")

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user_username = cursor.fetchone()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_email = cursor.fetchone()

    if user_email:
        raise CustomRequestError("Email already exists", 400)

    if user_username:
        raise CustomRequestError("Username already exists", 400)

    # Insert the user into the database
    user_id = str(uuid.uuid4())[:20]
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    sql = "INSERT INTO users (user_id, fullname, username, contact_number, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (user_id, fullname, username, contact_number, email, hashed_password))
    connection.commit()

    # Login the user immediately
    sql = "SELECT user_id FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()
    token = create_access_token(identity=user['user_id'])

    return redirect('login_page')
