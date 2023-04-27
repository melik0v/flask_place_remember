import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
lm = LoginManager(app)

from place_remember import routes
