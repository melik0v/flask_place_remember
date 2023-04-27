from place_remember.authorization import init_config
from place_remember import app, db, lm
from place_remember.models import User

init_config(app)
# lm.login_view('login')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
