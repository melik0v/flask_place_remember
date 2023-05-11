import os

from dotenv import load_dotenv
from flask import Flask

from place_remember.authorization.routes import auth
from place_remember.extensions import db, lm
from place_remember.models import User
from place_remember.routes import main

dotenv_path = ".env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def create_app(database_uri="sqlite:///database.db", csrf=True):
    app = Flask(__name__)

    app.config["WTF_CSRF_ENABLED"] = csrf
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    lm.init_app(app)

    @lm.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
