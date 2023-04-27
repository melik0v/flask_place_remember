from datetime import datetime

from flask_login import (
    UserMixin,
)
from place_remember import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(256), nullable=False)
    access_token = db.Column(db.String(256), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'<user {self.id}>'

