import os

from flask import Flask
from sqlalchemy import create_engine


app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])

# Create an enging that stores data in the env database
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

from petsrus.views import main
