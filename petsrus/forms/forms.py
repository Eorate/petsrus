from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Please enter your username"),
            Length(
                min=4,
                max=25,
                message="Username must be between 4 to 25 characters in length",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Please enter your password"),
            EqualTo("confirm_password", message="Passwords must match"),
            Length(min=8, message="Password should be aleast 8 characters in length"),
        ],
    )
    confirm_password = PasswordField("Confirm password")
    email_address = StringField(
        "Email address",
        validators=[
            DataRequired(message="Please enter your email address"),
            Email(message="Please enter a valid email address"),
            Length(min=6, max=35),
        ],
    )
    telephone = StringField("Telephone")
    country = StringField("Country")
    register = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(message="Please enter your username")]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Please enter your password")]
    )
    login = SubmitField("Login")


class PetForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Please enter a name"),
            Length(
                min=2,
                max=24,
                message="Name must be between 2 to 25 characters in length",
            ),
        ],
    )
    date_of_birth = DateField(
        "Date of Birth",
        format="%Y-%m-%d",
        validators=[DataRequired(message="Please enter a Date of Birth (YYYY-MM-DD)")],
    )
    species = StringField(
        "Species",
        validators=[
            DataRequired(message="Please provide species details"),
            Length(
                min=4,
                max=10,
                message="Species must be between 4 to 10 characters in length",
            ),
        ],
    )
    breed = StringField(
        "Breed",
        validators=[
            DataRequired(message="Please provide breed details"),
            Length(
                min=5,
                max=25,
                message="Breed must be between 5 to 25 characters in length",
            ),
        ],
    )
    sex = StringField(
        "Sex",
        validators=[
            DataRequired(message="Please provide pet sex details"),
            Length(min=1, max=1, message="Enter M or F for sex"),
        ],
    )
    colour_and_identifying_marks = StringField("Colour and identifying marks")
    save = SubmitField("Save")
