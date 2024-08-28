import pytest
from fumble.db import get_db


def test_index(client, auth):
    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'Chats' in response.data
