from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, current_app
import uuid
import bcrypt
from flask_jwt_extended import create_access_token
from ..database import get_connection
from ..utils.helpers import response, dict_except
from ..utils.errors import CustomRequestError, catch_exception
from ..utils.mailer import send_mail
from ..utils.variables import APP_LOGO, APP_URL
from ..database.notification_table import create_notification
from datetime import timedelta


auth = Blueprint("auth", __name__)
app = current_app

connection, cursor = get_connection()

# LOGIN ROUTE FOR USERS
@auth.post("/")
@catch_exception
def login_page():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    sql = "SELECT * FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        raise CustomRequestError("Invalid email or password", 400)

    # GENERATE THE JWT TOKEN
    expiry_time = timedelta(days=7)
    token = create_access_token(identity=user['user_id'], expires_delta=expiry_time)

    data = dict_except(user, "password")
    return response("Log in successful", {"token": token, "user": data})


# REGISTRATION ROUTE FOR USERS
@auth.post('/signup')
@catch_exception
def handle_signup_page():
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

    if user_email:
        raise CustomRequestError("Email already exists", 400)

    if user_username:
        raise CustomRequestError("Username already exists", 400)

    # INSERT THE USER INTO THE TABLE
    user_id = str(uuid.uuid4())[:20]
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    sql = "INSERT INTO users (user_id, fullname, username, contact_number, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (user_id, fullname, username, contact_number, email, hashed_password))
    connection.commit()

    # SEND EMAIL
    subject = "Welcome to PlantNest - Where Nature Finds a Home! 🌿"
    body = render_template('email/welcome.html', APP_URL=APP_URL, APP_LOGO=APP_LOGO, name=fullname)
    send_mail(app, subject, [email], body, is_html=True)

    # NOTIFY THE ADMIN A NEW USER WAS CREATED
    create_notification("New user", "A new user just joined", "ADMIN")

    # LOGIN IN THE USER IMMEDIATELY AFTER REGISTRATION
    sql = "SELECT user_id, email, fullname, username, contact_number FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    # SET EXPIRY TIME [7d]
    expiry_time = timedelta(days=7)
    token = create_access_token(identity=user['user_id'], expires_delta=expiry_time)
    return response("User registration successful", {"token": token, "user": user})
