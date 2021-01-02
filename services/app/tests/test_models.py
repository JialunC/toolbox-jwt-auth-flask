import jwt
import pytest
from app.model import User

def test_new_user(client):
    user = User(pytest.EMAIL, pytest.PASSWORD)
    assert user.email == 'tom@gmail.com'
    assert user.password_hash != pytest.PASSWORD
    assert user.check_password(pytest.PASSWORD)
    assert not user.check_password('password')

def test_decode_auth_token(client, init_database, init_user):
    user = init_user
    token = user.get_auth_token()
    uuid = user.decode_auth_token(token)
    assert uuid == user.uuid