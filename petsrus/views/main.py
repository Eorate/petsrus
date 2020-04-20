from flask import render_template, redirect, request, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user

from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from sentry_sdk import capture_exception

from petsrus.petsrus import app, engine, login_manager
from petsrus.models.models import Base, Pet, User
from petsrus.forms.forms import LoginForm, PetForm, RegistrationForm


Base.metadata.bind = engine
Base.metadata.create_all()
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        try:
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                email_address=form.email_address.data,
                telephone=form.telephone.data,
                country=form.country.data,
            )
            db_session.add(user)
            db_session.commit()
            flash("Thanks for registering", "info")
        except exc.IntegrityError as error:
            capture_exception(error)
            db_session.rollback()
            app.logger.error(error.orig)
            flash(
                "Sorry, Username '{}' or Email '{}' is already in use".format(
                    form.username.data, form.email_address.data
                ),
                "danger",
            )
            return render_template("register.html", form=form)
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)


@app.route("/add_pet", methods=["GET", "POST"])
@login_required
def add_pet():
    form = PetForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            pet = Pet(
                name=form.name.data,
                date_of_birth=form.date_of_birth.data,
                species=form.species.data,
                breed=form.breed.data,
                sex=form.sex.data,
                colour_and_identifying_marks=form.colour_and_identifying_marks.data,
            )
            db_session.add(pet)
            db_session.commit()
            flash("Saved Pet", "success")
            return redirect(url_for("index"))
        except Exception as exc:
            capture_exception(exc)
    else:
        return render_template("pets.html", add=True, form=form)


# https://stackoverflow.com/questions/47735329/updating-a-row-using-sqlalchemy-orm
@app.route("/edit_pet/<int:pet_id>", methods=["GET", "POST"])
@login_required
def edit_pet(pet_id):
    pet = db_session.query(Pet).filter_by(id=pet_id).first()
    form = PetForm(obj=pet)

    if request.method == "POST" and form.validate():
        try:
            pet = db_session.query(Pet).get(pet_id)

            pet.name = (form.name.data,)
            pet.date_of_birth = (form.date_of_birth.data,)
            pet.species = (form.species.data,)
            pet.breed = (form.breed.data,)
            pet.sex = (form.sex.data,)
            pet.colour_and_identifying_marks = (form.colour_and_identifying_marks.data,)

            db_session.commit()
            flash("Updated Pet Details", "success")
            return redirect(url_for("index"))
        except Exception as exc:
            capture_exception(exc)
    else:
        return render_template("pets.html", edit=True, form=form, pet_id=pet_id)


@app.route("/view_pet/<int:pet_id>", methods=["GET"])
@login_required
def view_pet(pet_id):
    pet = db_session.query(Pet).filter_by(id=pet_id).first()
    schedules = db_session.query(Schedule).filter_by(pet_id=pet_id).all()
    return render_template("pet_details.html", pet=pet, schedules=schedules)


# https://dzone.com/articles/flask-101-filtering-searches-and-deleting-data
@app.route("/delete/<int:pet_id>", methods=["POST"])
@login_required
def delete_pets(pet_id):
    if request.method == "POST":
        try:
            pet = db_session.query(Pet).get(pet_id)
            db_session.delete(pet)
            db_session.commit()
            flash("Deleted Pet Details", "success")
            return redirect(url_for("index"))
        except Exception as exc:
            capture_exception(exc)


@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = (
            db_session.query(User).filter(User.username == form.username.data).first()
        )
        if user and check_password_hash(user.password, form.password.data):
            user.authenticated = True
            login_user(user, remember=True)
            return redirect(url_for("index"))
        else:
            flash("Sorry, username or password was incorrect", "danger")
            return render_template("index.html", form=form)
    else:
        pets = db_session.query(Pet).all()
        return render_template("index.html", form=form, pets=pets)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
