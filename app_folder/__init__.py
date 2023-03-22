from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#no idea? we are initializing an app object, but what does that mean?
app = Flask(__name__)

#setting the configuration of the flask app based on environment variables
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.ProductionConfig")

#initializing a SQLAlchemy obbject and passing app. What is this?
db = SQLAlchemy(app)

from app_folder import views