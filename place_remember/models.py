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


class Memory(db.Model):
    __tablename__ = 'memories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    description = db.Column(db.String)
    place = db.Column(db.String)

    def __repr__(self):
        return f'<memory {self.name}>'


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    memory = db.Column(db.Integer, db.ForeignKey(Memory.id))
    image = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'<image from memory {self.memory}>'
