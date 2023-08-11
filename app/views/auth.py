from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, current_app, flash
from functools import wraps
import uuid
import bcrypt
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


@auth.post("/")
def handle_login_page():
    try:
        data = request.form
        email = data.get("email")
        password = data.get("password")

        sql = "SELECT * FROM admins WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        print(user)
        print("Check something")

        if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            raise CustomRequestError("Invalid email or password", 400)

        # GENERATE THE JWT TOKEN
        token = create_access_token(identity=user["user_id"])
        print(token)
        flash("Login successful", "success")
    except Exception as e:
        print(e)
    return redirect("/dashboard")


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
    cursor.execute(sql, ("ADMIN", fullname, image, email, hashed_password))
    connection.commit()

    # Log the user in immediately after signup
    session["admin"] = True
    session["admin_id"] = admin_id  # Store the admin's ID in the session

    # Redirect the admin to the dashboard
    flash("Registration successful", "success")
    return redirect('/')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect("/")
