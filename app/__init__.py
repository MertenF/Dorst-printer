from flask import Flask
from flask_cors import CORS
from waitress import serve

from . import db

from app import log

app = Flask(__name__)

CORS(app)
db.init_app(app)

from app import views

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=443)
