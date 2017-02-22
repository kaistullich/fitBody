import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from fitBody.views import my_view
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import fields, widgets

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(my_view)

# app.debug used for Toolbar Extension
# app.debug = True
# toolbar = DebugToolbarExtension(app)

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


# Create the WYSIWYG editor
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


# Create models (User Registration DB)
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50))
    username = db.Column(db.String(20))
    hash = db.Column(db.String(350))


# Create class to be able to use the WYSIWYG editor
class ProductEdit(ModelView):
    # form_overrides = dict(description=CKTextAreaField)
    create_template = 'create.html'
    edit_template = 'edit.html'

    # Formats the description columns since it will be very long
    def _description_formatter(view, model):
        # If the description column is empty it will place an empty string for formatting purposes
        if model.description is None:
            return ""
        # If description column is not empty, it will only show up to 19 characters
        return model.description[:20]

    column_formatters = {
        'description': _description_formatter,
    }

# # Add views
admin.add_view(ProductEdit(Registration, db.session))
