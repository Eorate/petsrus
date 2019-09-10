from flask import render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import sessionmaker

from petsrus.petsrus import app, engine
from petsrus.models.models import Base, Pet, User
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
        user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            email_address=form.email_address.data,
            telephone=form.telephone.data,
            country=form.country.data,
        )
        session.add(user)
        session.commit()
        flash("Thanks for registering", "info")
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)


@app.route("/pets", methods=["GET"])
def pets():
    pets = session.query(Pet).all()
    return render_template("pets.html", pets=pets), 200
