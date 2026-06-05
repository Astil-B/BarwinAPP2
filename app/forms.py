from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    IntegerField,
    DecimalField,
    SelectField,
    TextAreaField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, Optional, Regexp, NumberRange, EqualTo

from app.choices import ROLE_CHOICES, CATEGORY_CHOICES, USER_TYPE_CHOICES

EMAIL_RE = r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$"
PHONE_RE = r"^(\+45|0045)?[2-9]\d{7}$"
DATE_RE = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
DT_HINT = "Format: DD-MM-YYYY HH:MM"


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=50)])
    full_name = StringField("Full name", validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    password_repeat = PasswordField(
        "Repeat password", validators=[DataRequired(), EqualTo("password", "Passwords must match.")]
    )
    user_type = SelectField("Account type", choices=USER_TYPE_CHOICES, validators=[DataRequired()])
    submit = SubmitField("Sign up")


class EventForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    date = StringField(
        "Date", validators=[DataRequired(), Regexp(DATE_RE, message="Date must be YYYY-MM-DD.")]
    )
    location = StringField("Location", validators=[Optional(), Length(max=200)])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Save event")


class ShiftForm(FlaskForm):
    event_id = SelectField("Event", coerce=int, validators=[DataRequired()])
    role = SelectField("Role", choices=ROLE_CHOICES, validators=[DataRequired()])
    start_time = StringField("Start time", validators=[DataRequired()])
    end_time = StringField("End time", validators=[DataRequired()])
    capacity = IntegerField("Capacity", validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField("Save shift")


class SignupActionForm(FlaskForm):
    volunteer_id = SelectField("Volunteer", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Sign up")


class VolunteerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField(
        "Email", validators=[DataRequired(), Regexp(EMAIL_RE, message="Invalid email address.")]
    )
    phone = StringField(
        "Phone",
        validators=[Optional(), Regexp(PHONE_RE, message="Invalid Danish phone number.")],
    )
    submit = SubmitField("Save volunteer")


class DrinkForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    category = SelectField("Category", choices=CATEGORY_CHOICES, validators=[DataRequired()])
    price_dkk = DecimalField("Price (DKK)", places=2, validators=[DataRequired(), NumberRange(min=0)])
    unit = StringField("Unit", validators=[Optional(), Length(max=20)])
    submit = SubmitField("Save drink")


class SaleForm(FlaskForm):
    event_id = SelectField("Event", coerce=int, validators=[DataRequired()])
    drink_id = SelectField("Drink", coerce=int, validators=[DataRequired()])
    volunteer_id = SelectField("Sold by", coerce=int, validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField("Record sale")
