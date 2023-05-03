from flask_login import current_user, login_user

from place_remember.models import Memory, User
from place_remember import db


def test_login_page(client):
    response = client.get('/')
    assert b'<title>Place Remember</title>' in response.data


def test_add_memory(client, app):
    with app.test_request_context():
        client.post('/memories/create', data={
            'name': 'test name',
            'place': '92.852571,56.010566',
            'description': 'test_description',
            'submit': True
        })
        assert db.session.query(Memory).count() == 1
        assert db.session.query(Memory).first().name == 'test name'


def test_get_memory_list(client, app):
    with app.test_request_context():
        # mock user
        test_user = db.session.query(User).first()
        login_user(test_user)

        # mock memory
        test_memory_1 = Memory(
            name='test_name_1',
            user_id=test_user.id,
            description='test_desc_1',
            place='92.852571,56.010566',
        )

        test_memory_2 = Memory(
            name='test_name_2',
            user_id=test_user.id,
            description='test_desc_2',
            place='92.852571,56.010566',
        )

        db.session.add(test_memory_1)
        db.session.add(test_memory_2)
        db.session.commit()

        memories = db.session.query(Memory).filter(Memory.user_id == current_user.get_id()).all()

        response = client.get('/memories', query_string={
            'user': test_user,
            'memories': memories
        })

    assert response.status_code == 200
    assert b'<h3>test_name_1</h3>' in response.data
    assert b'<h3>test_name_2</h3>' in response.data


def test_get_memory_detail(client, app):
    with app.test_request_context():
        # mock user
        test_user = db.session.query(User).first()
        login_user(test_user)

        # mock memory
        test_memory_1 = Memory(
            name='test_name_1',
            user_id=test_user.id,
            description='test_desc_1',
            place='92.852571,56.010566',
        )

        db.session.add(test_memory_1)
        db.session.commit()

        memory = Memory.query.filter(Memory.id == test_memory_1.id).first()

        response = client.get('/memories/1', query_string={
            'user': current_user,
            'object': memory
        })

    assert response.status_code == 200
    assert b'<h1>test_name_1</h1>' in response.data
    assert b'<span class="description">test_desc_1</span>' in response.data


def test_delete_memory(client, app):
    with app.test_request_context():
        # mock user
        test_user = db.session.query(User).first()
        login_user(test_user)

        # mock memory
        test_memory_1 = Memory(
            name='test_name_1',
            user_id=test_user.id,
            description='test_desc_1',
            place='92.852571,56.010566',
        )

        db.session.add(test_memory_1)
        db.session.commit()

        assert db.session.query(Memory).count() == 1
        assert db.session.query(Memory).first() == test_memory_1

        client.get('/memories/1/delete')

        assert db.session.query(Memory).count() == 0
        assert db.session.query(Memory).first() is None


def test_memory_edit(client, app):
    with app.test_request_context():
        # mock user
        test_user = db.session.query(User).first()
        login_user(test_user)

        # mock memory
        test_memory_1 = Memory(
            name='old name',
            user_id=test_user.id,
            description='old description',
            place='92.852571,56.010566',
        )

        db.session.add(test_memory_1)
        db.session.commit()

        old_name = test_memory_1.name
        old_desc = test_memory_1.description
        old_place = test_memory_1.place
        old_id = test_memory_1.id

        client.post('/memories/1/edit', data={
            'name': 'new name',
            'place': '92.852571,56.010566',
            'description': 'new description',
            'submit': True
        })

        new_name = test_memory_1.name
        new_desc = test_memory_1.description
        new_place = test_memory_1.place
        new_id = test_memory_1.id

        assert old_id == new_id
        assert old_place == new_place
        assert old_name != new_name
        assert old_desc != new_desc
