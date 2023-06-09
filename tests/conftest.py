import pytest

from place_remember import create_app, db
from place_remember.models import User


@pytest.fixture()
def app():
    app = create_app("sqlite://", csrf=False)
    app.config["LOGIN_DISABLED"] = True
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "TEST"
    with app.test_request_context():
        db.create_all()
        test_user = User(
            social_id="test_id",
            first_name="test_name",
            last_name="test_last_name",
            access_token="test_token",
            avatar="test_avatar_link",
        )
        db.session.add(test_user)
        db.session.commit()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
