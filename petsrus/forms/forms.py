from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from petsrus.forms.validators import FutureDate, PastDate
from petsrus.models.models import Repeat, Repeat_cycle
from wtforms import (
    IntegerField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import DateField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    InputRequired,
    Length,
    Optional,
)


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username:",
        validators=[
            InputRequired(message="Please enter your username"),
            Length(
                min=4,
                max=25,
                message="Username must be between 4 to 25 characters in length",
            ),
        ],
    )
    password = PasswordField(
        "Password:",
        validators=[
            InputRequired(message="Please enter your password"),
            EqualTo("confirm_password", message="Passwords must match"),
            Length(min=8, message="Password should be aleast 8 characters in length"),
        ],
    )
    confirm_password = PasswordField("Confirm password:")
    email_address = StringField(
        "Email address:",
        validators=[
            InputRequired(message="Please enter your email address"),
            Email(message="Please enter a valid email address"),
            Length(min=6, max=35),
        ],
    )
    telephone = StringField("Telephone:")
    country = StringField("Country:")
    register = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(
        "Username:", validators=[InputRequired(message="Please enter your username")]
    )
    password = PasswordField(
        "Password:", validators=[InputRequired(message="Please enter your password")]
    )
    login = SubmitField("Login")


class PetForm(FlaskForm):
    name = StringField(
        "Name:",
        validators=[
            InputRequired(message="Please enter a name"),
            Length(
                min=2,
                max=24,
                message="Name must be between 2 to 25 characters in length",
            ),
        ],
    )
    date_of_birth = DateField(
        "Date of Birth:",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="Please enter a Date of Birth (YYYY-MM-DD)"),
            PastDate(message="Please enter a date before {}".format(date.today())),
        ],
    )
    species = StringField(
        "Species:",
        validators=[
            InputRequired(message="Please provide species details"),
            Length(
                min=4,
                max=10,
                message="Species must be between 4 to 10 characters in length",
            ),
        ],
    )
    breed = StringField(
        "Breed:",
        validators=[
            InputRequired(message="Please provide breed details"),
            Length(
                min=5,
                max=25,
                message="Breed must be between 5 to 25 characters in length",
            ),
        ],
    )
    sex = StringField(
        "Sex:",
        validators=[
            InputRequired(message="Please provide pet sex details"),
            Length(min=1, max=1, message="Enter M or F for sex"),
        ],
    )
    colour_and_identifying_marks = StringField("Colour and identifying marks:")
    save = SubmitField("Save")


class PetScheduleForm(FlaskForm):
    pet_id = IntegerField("Pet id")
    date_of_next = DateField(
        "Date of Next:",
        format="%Y-%m-%d",
        validators=[
            InputRequired(message="Please enter the Date (YYYY-MM-DD)"),
            FutureDate(
                message="Please enter a date greater than today {}".format(date.today())
            ),
        ],
    )
    repeats = RadioField(
        "Repeats:",
        choices=Repeat.__values__,
        validators=[InputRequired(message="Please select either Yes or No")],
    )
    repeat_cycle = RadioField(
        "Repeat Cycle:", choices=Repeat_cycle.__values__, validators=[Optional()]
    )
    schedule_type = SelectField(u"Schedule Types", coerce=int)
    save = SubmitField("Save")


class ChangePetPhotoForm(FlaskForm):
    photo = FileField()
    save = SubmitField("Upload Photo")
