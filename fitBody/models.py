import sqlite3

from wtforms import BooleanField, StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length, EqualTo

sqlite_file = 'fitBody_registration.sqlite'
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()


class RegistrationForm(FlaskForm):
    username = StringField('Username:', [InputRequired(), Length(min=4, max=20)])
    email = StringField('Email Address:', [InputRequired(), Email('Invalid Email!')])
    password = PasswordField('Password:', [
        InputRequired(),
        Length(min=4, max=30),
        EqualTo('confirm', message='Passwords must match!')
    ])
    confirm = PasswordField('Confirm Password:')
    accept_tos = BooleanField("I accept the Terms of Service and Privacy", [InputRequired()])
