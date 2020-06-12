import os
import secrets
import traceback
from datetime import date

import boto3
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from PIL import Image, UnidentifiedImageError
from sentry_sdk import capture_exception
from sqlalchemy import desc, exc
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from petsrus.forms.forms import (ChangePetPhotoForm, LoginForm, PetForm,
                                 PetScheduleForm, RegistrationForm)
from petsrus.models.models import (Base, Pet, Repeat, Repeat_cycle, Schedule,
                                   Schedule_type, User)
from petsrus.petsrus import app, engine, login_manager

Base.metadata.bind = engine
Base.metadata.create_all()
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Dimensions of resized pet images
WIDTH = 400
HEIGHT = 252


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
            flash(
                "An unexpected issue occured while attempting to add a pet", "danger",
            )
            app.logger.error(traceback.format_exc())
            capture_exception(exc)
            return render_template("pets.html", add=True, form=form)
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
            app.logger.error(traceback.format_exc())
            capture_exception(exc)
            flash(
                "An unexpected issue occured while attempting to update pet", "danger",
            )
            return render_template("pets.html", edit=True, form=form, pet_id=pet_id)
    else:
        return render_template("pets.html", edit=True, form=form, pet_id=pet_id)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/update_pet_photo/<int:pet_id>", methods=["POST"])
@login_required
def update_pet_photo(pet_id):
    pet = db_session.query(Pet).filter_by(id=pet_id).first()
    if request.method == "POST":
        try:
            if "photo" not in request.files:
                flash("No file part", "danger")
                return redirect(url_for("view_pet", pet_id=pet_id))
            photo = request.files["photo"]
            # if user does not select file, the browser may also
            # submit an empty part without filename
            if photo.filename == "":
                flash("No selected photo", "danger")
            elif photo and allowed_file(photo.filename):
                random_hex = secrets.token_hex(8)
                output_size = (WIDTH, HEIGHT)
                filename = secure_filename(photo.filename)
                _, filename_extension = os.path.splitext(filename)
                photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                picture_filename = random_hex + filename_extension
                picture_path = os.path.join(
                    app.config["UPLOAD_FOLDER"], picture_filename
                )
                with Image.open(
                    os.path.join(app.config["UPLOAD_FOLDER"], filename)
                ) as img:
                    new_image = img.resize(output_size)
                    new_image.save(picture_path)
                    s3_client = boto3.client(
                        "s3", endpoint_url=app.config["BACKBLAZE_URL"]
                    )
                    s3_client.upload_file(
                        os.path.join(app.config["UPLOAD_FOLDER"], picture_filename),
                        app.config["S3_BUCKET"],
                        picture_filename,
                        ExtraArgs={
                            "ContentType": "image/{}".format(filename_extension)
                        },
                    )
                    pet.photo = picture_filename
                    db_session.commit()
                    flash("Changed Pet Photo", "success")
            else:
                flash("Photo type not allowed. Use png, gif, jpeg or jpg", "danger")
        except UnidentifiedImageError as error:
            flash("Unidentified Image Error", "danger")
            app.logger.error(error)
        except Exception as exc:
            flash(
                "An unexpected issue occured while attempting to update pet photo",
                "danger",
            )
            app.logger.error(traceback.format_exc())
            capture_exception(exc)
        return redirect(url_for("view_pet", pet_id=pet_id))


@app.route("/view_pet/<int:pet_id>", methods=["GET"])
@login_required
def view_pet(pet_id):
    pet = db_session.query(Pet).filter_by(id=pet_id).first()
    form = ChangePetPhotoForm()
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
        "pet_details.html",
        bucket_name=app.config["S3_BUCKET"],
        change_photo_form=form,
        due_schedules=due,
        past_schedules=past,
        pet=pet,
        uploaded_image_url=app.config["UPLOADED_IMAGE_URL"],
    )


# https://dzone.com/articles/flask-101-filtering-searches-and-deleting-data
@app.route("/delete_pet/<int:pet_id>", methods=["POST"])
@login_required
def delete_pet(pet_id):
    if request.method == "POST":
        try:
            pet = db_session.query(Pet).get(pet_id)
            db_session.delete(pet)
            db_session.commit()
            flash("Deleted Pet Details", "success")
        except Exception as exc:
            flash(
                "An unexpected issue occured while attempting to delete this pet",
                "danger",
            )
            app.logger.error(traceback.format_exc())
            capture_exception(exc)
        return redirect(url_for("index"))


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
        except Exception as exc:
            flash(
                "An unexpected issue occured while attempting to add a schedule",
                "danger",
            )
            app.logger.error(traceback.format_exc())
            capture_exception(exc)
        return redirect(url_for("view_pet", pet_id=pet_id))
    else:
        return render_template("pet_schedule.html", form=form, pet_id=pet_id)


@app.route("/delete_schedule/<int:schedule_id>", methods=["POST"])
@login_required
def delete_schedule(schedule_id):
    if request.method == "POST":
        schedule = db_session.query(Schedule).get(schedule_id)
        try:
            db_session.delete(schedule)
            db_session.commit()
            flash("Deleted Pet Schedule", "success")
        except Exception as exc:
            flash(
                "An unexpected issue occured while attempting to delete a schedule",
                "danger",
            )
            app.logger.error(traceback.format_exc())
            capture_exception(exc)
        return redirect(url_for("view_pet", pet_id=schedule.pet_id))


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
