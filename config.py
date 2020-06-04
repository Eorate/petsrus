import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    UPLOAD_FOLDER = tempfile.gettempdir()
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB


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

    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
    if not AWS_ACCESS_KEY:
        raise ValueError("No AWS ACCESS KEY")

    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not AWS_SECRET_ACCESS_KEY:
        raise ValueError("No AWS SECRET ACCESS KEY")

    AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")
    if not AWS_DEFAULT_REGION:
        raise ValueError("No AWS DEFAULT REGION")

    S3_BUCKET = os.environ.get("S3_BUCKET")
    if not S3_BUCKET:
        raise ValueError("No S3 BUCKET")

    BACKBLAZE_URL = os.environ.get("BACKBLAZE_URL")
    if not BACKBLAZE_URL:
        raise ValueError("No BackBlaze url provided")

    UPLOADED_IMAGE_URL = os.environ.get("UPLOADED_IMAGE_URL")
    if not UPLOADED_IMAGE_URL:
        raise ValueError("No Uploaded Image url provided")


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

    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
    if not AWS_ACCESS_KEY:
        raise ValueError("No AWS ACCESS KEY")

    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not AWS_SECRET_ACCESS_KEY:
        raise ValueError("No AWS SECRET ACCESS KEY")

    AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")
    if not AWS_DEFAULT_REGION:
        raise ValueError("No AWS DEFAULT REGION")

    S3_BUCKET = os.environ.get("S3_BUCKET")
    if not S3_BUCKET:
        raise ValueError("No S3 BUCKET")

    BACKBLAZE_URL = os.environ.get("BACKBLAZE_URL")
    if not BACKBLAZE_URL:
        raise ValueError("No BackBlaze url provided")

    UPLOADED_IMAGE_URL = os.environ.get("UPLOADED_IMAGE_URL")
    if not UPLOADED_IMAGE_URL:
        raise ValueError("No Uploaded Image url provided")


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

    S3_BUCKET = os.environ.get("S3_BUCKET")
    if not S3_BUCKET:
        raise ValueError("No S3 BUCKET")

    BACKBLAZE_URL = os.environ.get("BACKBLAZE_URL")
    if not BACKBLAZE_URL:
        raise ValueError("No BackBlaze url provided")

    UPLOADED_IMAGE_URL = os.environ.get("UPLOADED_IMAGE_URL")
    if not UPLOADED_IMAGE_URL:
        raise ValueError("No Uploaded Image url provided")

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS", default=False
    )

    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    LOGIN_DISABLED = True
