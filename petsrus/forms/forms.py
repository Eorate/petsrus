from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
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
