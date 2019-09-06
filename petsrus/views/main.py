from flask import render_template, redirect, request, url_for, flash

from sqlalchemy.orm import sessionmaker

from petsrus.petsrus import app, engine
from petsrus.models.models import Base, Pet
from petsrus.forms.forms import RegistrationForm


Base.metadata.bind = engine
Base.metadata.create_all()
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        flash("Thanks for registering", "info")
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)


@app.route("/pets", methods=["GET"])
def pets():
    pets = session.query(Pet).all()
    return render_template("pets.html", pets=pets), 200
