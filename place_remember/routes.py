from flask import (
    redirect,
    url_for,
    flash,
    render_template,
    request,
)

from flask.views import (
    View
)

from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)
from place_remember import app, db
from place_remember.authorization import OAuthSignIn
from place_remember.models import User, Memory
from place_remember.pipeline import UserInfoVK, UserInfoGoogle
from place_remember.forms import AddMemoryForm, AddImageForm


@app.route('/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('show_memories'))
    return render_template('login_page.html')


@app.route('/memories')
def show_memories():
    memories = Memory.query.filter(Memory.user_id == current_user.get_id())
    return render_template('memory_list.html', user=current_user, memories=memories)


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
        return redirect(url_for('show_memories'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, token = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('login'))

    user = User.query.filter_by(social_id=social_id).first()

    match provider:
        case 'google':
            user_info = UserInfoGoogle(token)
        case 'vk':
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
            avatar=user_info.get_avatar()
        )
        db.session.add(user)
        db.session.commit()

    login_user(user, True)
    return redirect(url_for('login'))


@app.route('/memories/create', methods=['POST', 'GET'])
@login_required
def create_memory():
    memory_form = AddMemoryForm()
    image_form = AddImageForm()
    if memory_form.validate_on_submit() and request.method == 'POST':
        memory = Memory(
            name=memory_form.name.data,
            description=memory_form.description.data,
            place=memory_form.place.data,
            user_id=current_user.get_id()
        )
        db.session.add(memory)
        db.session.commit()
        return redirect(url_for('show_memories'))
    return render_template('memory_form.html', memory_form=memory_form, image_form=image_form, user=current_user)


@app.route('/memories/<int:memory_id>')
@login_required
def memory_detail(memory_id):
    memory = Memory.query.filter(Memory.id == memory_id).first()
    return render_template('memory_detail.html', object=memory, user=current_user)


@app.route('/memories/<int:memory_id>/edit', methods=['POST', 'GET'])
@login_required
def memory_edit(memory_id):
    image_form = AddImageForm()
    memory = db.session.get(Memory, memory_id)
    memory_form = AddMemoryForm(obj=memory)
    if memory_form.validate_on_submit() and request.method == 'POST':
        memory_form.populate_obj(memory)
        # memory.name = request.form['name'],
        # memory.description = request.form['description'],
        # memory.place = request.form['place'],
        # memory.user_id = current_user.get_id()
        db.session.commit()
        return redirect(url_for('memory_detail', memory_id=memory_id))
    return render_template('memory_form.html', memory_form=memory_form, image_form=image_form, user=current_user)


@app.route('/memories/<int:memory_id>/delete')
def memory_delete(memory_id):
    memory = Memory.query.get(memory_id)
    db.session.delete(memory)
    db.session.commit()
    return redirect(url_for('show_memories'))
