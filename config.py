import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = os.environ.get("DEBUG", default=False)
    if str(DEBUG).lower() in ("f", "false"):
        DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
    if not SECRET_KEY:
        raise ValueError("No secret key set for Flask application")

    SENTRY_URI = os.environ.get("SENTRY_URL", default=None)
    if not SENTRY_URI:
        raise ValueError("No sentry url provided for Flask application")

    SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", default=None)
    if not SENTRY_ENVIRONMENT:
        raise ValueError("No sentry project environment provided for Flask application")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", default=None)
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No database url provided for Flask application")


class DevelopmentConfig(Config):
    DEBUG = os.environ.get("DEBUG", default=False)
    if str(DEBUG).lower() in ("f", "false"):
        DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
    if not SECRET_KEY:
        raise ValueError("No secret key set for Flask application")

    SENTRY_URI = os.environ.get("SENTRY_URL", default=None)
    if not SENTRY_URI:
        raise ValueError("No sentry url provided for Flask application")

    SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", default=None)
    if not SENTRY_ENVIRONMENT:
        raise ValueError("No sentry project environment provided for Flask application")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", default=None)
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No database url provided for Flask application")

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS", default=False
    )


class TestingConfig(Config):
    DEBUG = os.environ.get("DEBUG", default=False)
    if str(DEBUG).lower() in ("f", "false"):
        DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
    if not SECRET_KEY:
        raise ValueError("No secret key set for Flask application")

    SENTRY_URI = os.environ.get("SENTRY_URL", default=None)
    if not SENTRY_URI:
        raise ValueError("No sentry url provided for Flask application")

    SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", default=None)
    if not SENTRY_ENVIRONMENT:
        raise ValueError("No sentry project environment provided for Flask application")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", default=None)
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No database url provided for Flask application")

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS", default=False
    )
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    LOGIN_DISABLED = True
