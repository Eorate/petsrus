import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = os.environ.get("DEBUG", default=False)
    if DEBUG.lower() in ("f", "false"):
        DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
    if not SECRET_KEY:
        raise ValueError("No secret key set for Flask application")

    DATABASE_URL = os.environ.get("DATABASE_URL", default=None)
    if not DATABASE_URL:
        raise ValueError("No database url provided for Flask application")


class DevelopmentConfig(Config):
    DEBUG = os.environ.get("DEBUG", default=False)
    if DEBUG.lower() in ("f", "false"):
        DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
    if not SECRET_KEY:
        raise ValueError("No secret key set for Flask application")

    DATABASE_URL = os.environ.get("DATABASE_URL", default=None)
    if not DATABASE_URL:
        raise ValueError("No database url provided for Flask application")


class TestingConfig(Config):
    DEBUG = os.environ.get("DEBUG", default=False)
    if DEBUG.lower() in ("f", "false"):
        DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
    if not SECRET_KEY:
        raise ValueError("No secret key set for Flask application")

    DATABASE_URL = os.environ.get("DATABASE_URL", default=None)
    if not DATABASE_URL:
        raise ValueError("No database url provided for Flask application")
