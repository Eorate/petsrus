import traceback
from datetime import date

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from sentry_sdk import capture_exception
from sqlalchemy import desc, exc
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from petsrus.forms.forms import LoginForm, PetForm, PetScheduleForm, RegistrationForm
from petsrus.models.models import (
    Base,
    Pet,
    Repeat,
    Repeat_cycle,
    Schedule,
    Schedule_type,
    User,
)
from petsrus.petsrus import app, engine, login_manager

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
            app.logger.error(traceback.format_exc)
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
            app.logger.error(traceback.format_exc)
            capture_exception(exc)
    else:
        return render_template("pets.html", edit=True, form=form, pet_id=pet_id)


@app.route("/view_pet/<int:pet_id>", methods=["GET"])
@login_required
def view_pet(pet_id):
    pet = db_session.query(Pet).filter_by(id=pet_id).first()
    due = (
        db_session.query(Schedule)
        .filter(Schedule.pet_id == pet_id, Schedule.date_of_next >= date.today())
        .order_by(desc(Schedule.date_of_next))
        .all()
    )
    past = (
        db_session.query(Schedule)
        .filter(Schedule.pet_id == pet_id, Schedule.date_of_next < date.today())
        .order_by(desc(Schedule.date_of_next))
        .all()
    )
    return render_template(
        "pet_details.html", pet=pet, due_schedules=due, past_schedules=past
    )


# https://dzone.com/articles/flask-101-filtering-searches-and-deleting-data
@app.route("/delete_pet/<int:pet_id>", methods=["POST"])
@login_required
def delete_pet(pet_id):
    if request.method == "POST":
        try:
            schedule = db_session.query(Schedule).get(pet_id)
            pet = db_session.query(Pet).get(pet_id)
            if schedule:
                db_session.delete(schedule)
            db_session.delete(pet)
            db_session.commit()
            flash("Deleted Pet Details", "success")
            return redirect(url_for("index"))
        except Exception as exc:
            app.logger.error(traceback.format_exc)
            capture_exception(exc)


@app.route("/add_schedule/<int:pet_id>", methods=["GET", "POST"])
@login_required
def add_schedule(pet_id):
    form = PetScheduleForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            pet = db_session.query(Pet).filter_by(id=pet_id).first()
            form.schedule_type.choices = [Schedule_type.__values__]
            form.repeats.choices = [Repeat.__values__]
            form.repeat_cycle.choices = [Repeat_cycle.__values__]
            pet_schedule = Schedule(
                pet_id=pet.id,
                date_of_next=form.date_of_next.data,
                repeats=form.repeats.data,
                repeat_cycle=form.repeat_cycle.data,
                schedule_type=form.schedule_type.data,
            )
            db_session.add(pet_schedule)
            db_session.commit()
            flash("Saved Pet Schedule", "success")
            return redirect(url_for("index"))
        except Exception as exc:
            app.logger.error(traceback.format_exc)
            capture_exception(exc)
    else:
        return render_template("pet_schedule.html", form=form, pet_id=pet_id)


@app.route("/delete_schedule/<int:schedule_id>", methods=["POST"])
@login_required
def delete_schedule(schedule_id):
    try:
        if request.method == "POST":
            schedule = db_session.query(Schedule).get(schedule_id)
            db_session.delete(schedule)
            db_session.commit()
            flash("Deleted Pet Schedule", "success")
            return redirect(url_for("index"))
    except Exception as exc:
        app.logger.error(traceback.format_exc)
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
