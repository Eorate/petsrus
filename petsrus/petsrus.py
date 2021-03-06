import os

import sentry_sdk
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine

csrf = CSRFProtect()
login_manager = LoginManager()
app = Flask(__name__, static_url_path="/static")
csrf.init_app(app)
login_manager.init_app(app)

app.config.from_object(
    os.environ.get("APP_SETTINGS", default="config.DevelopmentConfig")
)

# Create an engine that stores data in the env database
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

# Initialise Sentry SDK
sentry_sdk.init(
    dsn=app.config["SENTRY_URI"], environment=app.config["SENTRY_ENVIRONMENT"]
)

from petsrus.views import main  # noqa isort:skip
