from flask import Flask

# Create the Flask app
app = Flask(__name__)
# Imported here to disable circular imports
from my_app.views import app
