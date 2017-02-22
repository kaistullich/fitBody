import sqlite3
from wtforms import Form, BooleanField, StringField, PasswordField, validators

sqlite_file = 'fitBody_registration.sqlite'
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()


class RegistrationForm(Form):
    username = StringField('Username:', [validators.Length(min=4, max=20)])
    email = StringField('Email Address:', [validators.Length(min=6, max=50)])
    password = PasswordField('Password:', [
        validators.DataRequired(),
        validators.Length(min=6, max=15),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password:')
    accept_tos = BooleanField("I accept the Terms of Service and Privacy", [validators.DataRequired()])
