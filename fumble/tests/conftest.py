import os
import tempfile

import pytest
from pyotp import totp
from fumble import create_app
from fumble.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as file:
    sql_data = file.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(sql_data)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test', mfa_secret='UL76UNQ3PAIZEBLPAUK4MEQQCSPM3Y5B'):
        self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

        return self._client.post(
            '/auth/mfa',
            data={
                'code': totp.TOTP(mfa_secret).now()
            }
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
