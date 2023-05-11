from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from place_remember.authorization.pipeline import (
    OAuthSignIn,
    UserInfoGoogle,
    UserInfoVK,
)
from place_remember.extensions import db
from place_remember.models import User

auth = Blueprint("auth", __name__)


@auth.route("/")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.show_memories"))
    return render_template("login_page.html")


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for(".login"))


@auth.route("/authorize/<provider>")
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for(".login"))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@auth.route("/callback/<provider>")
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("main.show_memories"))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, token = oauth.callback()
    if social_id is None:
        flash("Authentication failed.")
        return redirect(url_for(".login"))

    user = User.query.filter_by(social_id=social_id).first()

    match provider:
        case "google":
            user_info = UserInfoGoogle(token)
        case "vk":
            user_info = UserInfoVK(social_id, token)
        case _:
            user_info = None

    if not user:
        first_name, last_name = user_info.get_firstname_lastname()
        user = User(
            social_id=social_id,
            first_name=first_name,
            last_name=last_name,
            access_token=token,
            avatar=user_info.get_avatar(),
        )
        db.session.add(user)
        db.session.commit()

    login_user(user, True)
    return redirect(url_for(".login"))
