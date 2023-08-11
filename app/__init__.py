from flask import Flask, request, redirect, url_for, render_template
from .migrate import run_migrations
from flask_jwt_extended import  JWTManager
from .utils.helpers import response
from .utils.variables import APP_NAME, MAIL_SERVER, MAIL_PASSWORD, MAIL_PORT, APP_SECRET, MAIL_USERNAME, JWT_SECRET


def create_app():
	app = Flask(__name__)
	jwt = JWTManager(app)

	# RUN MIGRATIONS
	run_migrations()

	# ***** CONFIGS ***** #
	# APP CONFIGS
	app.config["APP_NAME"] = APP_NAME
	app.config["APP_SECRET"] = APP_SECRET
	app.config["SECRET_KEY"] = APP_SECRET
	app.config["JWT_SECRET_KEY"] = APP_SECRET

	# MAIL CONFIGS
	app.config['MAIL_SERVER'] = MAIL_SERVER
	app.config['MAIL_PORT'] = MAIL_PORT
	app.config['MAIL_USE_SSL'] = True
	app.config['MAIL_USERNAME'] = MAIL_USERNAME
	app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

	# ALL ADMIN ROUTES
	from .views import dashboard
	app.register_blueprint(dashboard)

	# TODO: REMEMBER TO FIX THIS
	from .views.auth import auth
	from app.apis.user import user
	app.register_blueprint(auth)
	app.register_blueprint(user)

	# API ENDPOINT
	from .apis import api
	app.register_blueprint(api, url_prefix="/api/v1")


	# ERROR ROUTES
	@app.errorhandler(404)
	def invalid_route(error):
		print("ERROR 404:", error)
		url = request.url
		# RETURN A JSON RESPONSE FOR API REQUESTS
		if "/api/v1" in url: return response("Invalid route", None, False)

		# REDIRECT
		return render_template("404.html", APP_NAME=APP_NAME)


	@app.errorhandler(Exception)
	def server_error(error):
		print("ERROR 500:", error)
		url = request.url
		if "/api/v1" in url: return response(str(error), None, False)

		# REDIRECT
		return render_template("500.html")

	return app