from setuptools import setup

setup(
    name="petsrus_cunning_locust",
    version="0.0.0",
    description="A flask application that keeps track of your pet details.",
    url="https://github.com/Eorate/petsrus.git",
    author="Tharlaw",
    author_email="tharlaw@example.com",
    license="LICENSE",
    packages=["petsrus"],
    include_package_data=True,
    install_requires=[
        "alembic",
        "boto3",
        "email-validator",
        "flask",
        "Flask-Login",
        "Flask-SQLAlchemy",
        "Flask-WTF",
        "gunicorn",
        "psycopg2",
        "Pillow",
        "SQLAlchemy",
        "Werkzeug",
        "sentry-sdk",
    ],
    zip_safe=False,
)
