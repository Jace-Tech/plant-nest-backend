from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, current_app
import uuid
import bcrypt
from flask_jwt_extended import create_access_token
from ..database import get_connection
from ..utils.helpers import response
from ..utils.errors import CustomRequestError
from ..utils.mailer import send_mail
from ..utils.variables import APP_LOGO, APP_URL
from ..database.notification_table import create_notification

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

    # GENERATE THE JWT TOKEN
    token = create_access_token(identity=user["user_id"])
    return response("Log in successful", token)


@auth.post('/signup')
def handle_signup_page():
    data = request.get_json()
    fullname = data.get("fullName")
    username = data.get("username")
    contact_number = data.get("contactNumber")
    email = data.get("email")
    password = data.get("password")

    print("Passed 1")
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user_username = cursor.fetchone()
    print("Passed 2")
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_email = cursor.fetchone()
    print("Passed 3")

    if user_email:
        raise CustomRequestError("Email already exists", 400)

    if user_username:
        raise CustomRequestError("Username already exists", 400)

    print("Passed 4")
    # INSERT THE USER INTO THE TABLE
    user_id = str(uuid.uuid4())[:20]
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    sql = "INSERT INTO users (user_id, fullname, username, contact_number, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (user_id, fullname, username, contact_number, email, hashed_password))
    connection.commit()
    print("Passed 5")

    # SEND EMAIL
    subject = "Welcome to PlantNest - Where Nature Finds a Home! 🌿"
    body = render_template('email/welcome.html', APP_URL=APP_URL, APP_LOGO=APP_LOGO, name=fullname)
    send_mail(app, subject, [email], body, is_html=True)
    print("Passed 6")

    # NOTIFY THE ADMIN A NEW USER WAS CREATED
    create_notification("New user", "A new user just joined", "ADMIN")

    # LOGIN IN THE USER IMMEDIATELY AFTER REGISTRATION
    sql = "SELECT user_id FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()
    print("Passed 7")

    token = create_access_token(identity=user['user_id'])
    print(token)
    return response("User registration successful", token)
