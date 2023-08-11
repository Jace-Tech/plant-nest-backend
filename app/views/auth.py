from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, current_app, flash
from functools import wraps
import uuid
import bcrypt
from flask_jwt_extended import create_access_token
from ..database import get_connection
from ..utils.helpers import response
from ..utils.errors import CustomError
from ..utils.uploader import upload_file
from ..utils.decorators import ensure_only_one_admin

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

        if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            raise CustomError("Invalid email or password")

        # SET LOGIN SESSIONS
        session["logged_in"] = True
        session["admin"] = user 

        # REDIRECT TO DASHBOARD
        flash("Login successful", "success")
        return redirect("/dashboard")
    
    except CustomError as e:
        flash(e.message, e.category)

    except Exception as e:
        flash(str(e), "error")
    return redirect("/")


@auth.get("/signup")
@ensure_only_one_admin
def signup_page():
    return render_template("signup.html")


@auth.post('/signup')
@ensure_only_one_admin
def handle_admin_sign_page():
    try:
        data = request.form
        fullname = data.get("fullName")
        email = data.get("email")
        password = data.get("password")

        cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
        user_email = cursor.fetchone()

        if user_email: raise CustomError("Email already exists")

        # UPLOAD IMAGE TO CLOUD
        image = request.files.get('image')
        image_url = upload_file(image, "admin_profile")

        # HASH PASSWORD
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # INSERT TO DATABASE
        sql = "INSERT INTO admins (admin_id, name, image, email, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, ("ADMIN", fullname, image_url.secure_url, email, hashed_password))
        connection.commit()

        # CHECK IF SUCCESSFUL
        if not cursor.rowcount: raise CustomError("Failed to create admin")

        # REDIRECT TO LOGIN
        flash("Registration successful", "success")
        return redirect('/')
    except CustomError as e:
        flash(e.message, e.category)

    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for('auth.signup_page'))

@auth.route('/logout')
def logout():
    session.clear()
    return redirect("/")
