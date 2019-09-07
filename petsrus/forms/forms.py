from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(message="Please enter your username")]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Please enter your password"),
            EqualTo("confirm_password", message="Passwords must match"),
        ],
    )
    confirm_password = PasswordField("Confirm password")
    email_address = StringField(
        "Email address",
        validators=[
            DataRequired(message="Please enter your email address"),
            Email(message="Please enter a valid email address"),
        ],
    )
    telephone = StringField("Telephone")
    country = StringField("Country")
    register = SubmitField("Register")
