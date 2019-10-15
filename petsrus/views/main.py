from flask import render_template, redirect, request, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user


from sqlalchemy.orm import sessionmaker

from petsrus.petsrus import app, engine, login_manager
from petsrus.models.models import Base, Pet, User
from petsrus.forms.forms import LoginForm, RegistrationForm


Base.metadata.bind = engine
Base.metadata.create_all()
DBSession = sessionmaker(bind=engine)
session = DBSession()


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = session.query(User).filter(User.username == form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            user.authenticated = True
            login_user(user, remember=True)
            pets = session.query(Pet).all()
            return redirect(url_for("pets", pets=pets))
        else:
            flash("Sorry, username or password was incorrect", "error")
            return render_template("index.html", form=form)
    else:
        return render_template("index.html", form=form)


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
@login_required
def pets():
    pets = session.query(Pet).all()
    return render_template("pets.html", pets=pets), 200


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
