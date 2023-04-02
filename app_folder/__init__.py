#Import flask, and SQLAlchemy classes from respectivee modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Initializing a Flask object named app, passed the name of the current python
#module, which Flask uses to locate resources like templates or static files
app = Flask(__name__)

#setting the configuration of the flask app based on environment variables
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.ProductionConfig")

#initializing a SQLAlchemy object and passing app creating a db connection
db = SQLAlchemy(app)
#importing all of our routing for the web site
from app_folder import views