from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)

@auth.get("/")
def login_page():
  return render_template("signin.html")