from dotenv import dotenv_values

ENV = dotenv_values()

# APP VARAIBLES
APP_SECRET = ENV['APP_SECRET']
APP_NAME = ENV['APP_NAME']

# JWT VARIABLES
JWT_SECRET = ENV['JWT_SECRET']

# CLOUDINARY VARIABLES
CLOUD_NAME = ENV['CLOUD_NAME']
CLOUD_API_KEY = ENV['CLOUD_API_KEY']
CLOUD_API_SECRET = ENV['CLOUD_API_SECRET']

# MAIL VARIBLES
MAIL_SERVER = ENV['MAIL_SERVER']
MAIL_PORT = ENV['MAIL_PORT']
MAIL_USERNAME = ENV['MAIL_USERNAME']
MAIL_PASSWORD = ENV['MAIL_PASSWORD']

# DATABASE VARIBLES
MYSQL_HOST = ENV['MYSQL_HOST']
MYSQL_USER = ENV['MYSQL_USER']
MYSQL_PASSWORD = ENV['MYSQL_PASSWORD']
MYSQL_DB = ENV['MYSQL_DB']
MYSQL_PORT = ENV['MYSQL_PORT']
