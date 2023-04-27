from flask import (
    redirect,
    url_for,
    flash,
    render_template,
)

from flask.views import (
    View
)

from flask_login import (
    current_user,
    login_user,
    logout_user,
)
from place_remember import app, db
from place_remember.authorization import OAuthSignIn
from place_remember.models import User
from place_remember.pipeline import UserInfoVK, UserInfoGoogle, UserInfo


@app.route('/')
def login():
    if current_user.is_authenticated:
        return render_template('base.html', user=current_user)
    return render_template('login_page.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('login'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, token = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('login'))

    user = User.query.filter_by(social_id=social_id).first()

    if provider == 'google':
        user_info = UserInfoGoogle(token)
    elif provider == 'vk':
        user_info = UserInfoVK(social_id, token)

    if not user:
        first_name, last_name = user_info.get_firstname_lastname()
        user = User(social_id=social_id, first_name=first_name, last_name=last_name, access_token=token,
                    avatar=user_info.get_avatar())
        db.session.add(user)
        db.session.commit()

    login_user(user, True)
    return redirect(url_for('login'))
