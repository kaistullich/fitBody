import os
import sqlite3

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField
from wtforms import fields, widgets
from wtforms.validators import InputRequired, Email, Length, EqualTo

from my_app import app

# Secret Key for cookies
app.secret_key = os.urandom(24)

# Instantiate the Boostrap app
Bootstrap(app)

# Configure the name of the DB
app.config['DATABASE_FILE'] = 'fitBody_registration.sqlite'

# Show full path to where DB is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/kai/github-projects/fitBody/fitBody_registration.sqlite'

# SQAlchemy Debug Purpose
app.config['SQLALCHEMY_ECHO'] = True

# Suppress warning when running app (SQLAlchemy uses significant overhead)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Pass Flask App into SQLAlchemy
db = SQLAlchemy(app)

# Creating the admin navbar with Boostrap
admin = Admin(app, template_mode='bootstrap3')


sqlite_file = 'fitBody_registration.sqlite'
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()


class Login(FlaskForm):
    """ Login form for all users"""
    username = StringField('Username:', [InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password:', [InputRequired(), Length(min=4, max=20)])


class RegistrationForm(FlaskForm):
    """ Registration form for new users"""
    username = StringField('Username:', [InputRequired(), Length(min=4, max=20)])
    email = StringField('Email Address:', [InputRequired(), Email('Invalid Email!')])
    password = PasswordField('Password:', [
        InputRequired(),
        Length(min=4, max=30),
        EqualTo('confirm', message='Passwords must match!')
    ])
    confirm = PasswordField('Confirm Password:')
    accept_tos = BooleanField("I accept the Terms of Service and Privacy", [InputRequired()])


class CKTextAreaWidget(widgets.TextArea):
    """ WYSIWYG Editor creation"""
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


class Admin(db.Model):
    """ Creates model for Admin database"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(350))


class Registration(db.Model):
    """ Creates a model for the Registration database table"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50))
    username = db.Column(db.String(20))
    password = db.Column(db.String(60))
    # description = db.Column(db.UnicodeText())


class RegistrationEdit(ModelView):
    """ Creates model view for Admin"""
    form_overrides = dict(description=CKTextAreaField)
    create_template = 'create.html'
    edit_template = 'edit.html'

    # Formats the description columns since it will be very long
    @staticmethod
    def _description_formatter(model):
        # If the description column is empty it will place an empty string for formatting purposes
        if model.description is None:
            return ""
        # If description column is not empty, it will only show up to 19 characters
        return model.description[:20]

    column_formatters = {
        'description': _description_formatter,
    }

# # Add views
admin.add_view(RegistrationEdit(Registration, db.session))
