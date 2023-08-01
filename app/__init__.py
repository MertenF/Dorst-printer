from flask import Flask
from flask_cors import CORS

from . import db

from app import log

app = Flask(__name__)

CORS(app)
db.init_app(app)

from app import views
