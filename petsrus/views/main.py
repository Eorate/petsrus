from flask import render_template

from sqlalchemy.orm import sessionmaker

from petsrus.petsrus import app, engine
from petsrus.models.models import Base, Pet


Base.metadata.bind = engine
Base.metadata.create_all()
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def login():
    return "Login Page"


@app.route("/pets", methods=["GET"])
def pets():
    pets = session.query(Pet).all()
    return render_template("pets.html", pets=pets), 200
