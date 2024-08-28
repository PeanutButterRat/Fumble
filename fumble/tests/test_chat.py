import pytest
from fumble.db import get_db


def test_create_room(client, auth):
    auth.login()
    response = client.post('/', data={'room': 'room_name'})

    assert response.headers["Location"] == '/room_name'
