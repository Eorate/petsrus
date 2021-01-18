import re

from setuptools import setup

with open("petsrus/semantic_release/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)


setup(
    name="petsrus_cunning_locust",
    version=version,
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
        "Flask==1.1.2",
        "Flask-Login",
        "Flask-SQLAlchemy",
        "Flask-WTF",
        "gunicorn",
        "psycopg2",
        "Pillow",
        "SQLAlchemy",
        "Werkzeug",
        "sentry-sdk",
        "WTForms==2.3.3",
    ],
    zip_safe=False,
)
