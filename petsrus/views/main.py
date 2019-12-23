from flask import render_template, redirect, request, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user


from sqlalchemy.orm import sessionmaker

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


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = (
            db_session.query(User).filter(User.username == form.username.data).first()
        )
        if user and check_password_hash(user.password, form.password.data):
            user.authenticated = True
            login_user(user, remember=True)
            pets = db_session.query(Pet).all()
            return redirect(url_for("index", pets=pets))
        else:
            flash("Sorry, username or password was incorrect", "error")
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)


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
        db_session.add(user)
        db_session.commit()
        flash("Thanks for registering", "info")
        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)


@app.route("/pets", methods=["GET", "POST"])
@login_required
def pets():
    form = PetForm(request.form)
    if request.method == "POST":
        if form.validate():
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
        else:
            return render_template("pets.html", form=form)
    elif request.method == "GET":
        pets = db_session.query(Pet).all()
        return render_template("pets.html", pets=pets, form=form)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
