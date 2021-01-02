import pytest
from unittest.mock import patch
from app.model import User
from app import utils
from jwt import (
    ExpiredSignatureError,
    InvalidTokenError
)

def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'status' in response.get_json()
    assert utils.SUCCESS in response.get_json().get('status')

def test_create_user(client, init_database):
    response = client.post(
        '/user',
        json=dict(
            email=pytest.EMAIL,
            password=pytest.PASSWORD,
        )
    )
    uuid = response.json['message']['uuid']
    user = User.query.filter_by(uuid=uuid).first()
    assert response.status_code == 201
    assert user.email == pytest.EMAIL
    assert user.check_password(pytest.PASSWORD)

def test_cannot_recreate_user(client, init_database, init_user):
    response = client.post(
        '/user',
        json=dict(
            email=pytest.EMAIL,
            password=pytest.PASSWORD,
        )
    )
    assert response.status_code == 404
    assert 'status' in response.get_json()
    assert utils.ERROR in response.get_json().get('status')
    assert utils.ACCOUNT_ALREADY_EXISTS in response.get_json().get('message')

def test_auth(client, init_database, init_user):
    response = client.post(
        '/auth',
        json=dict(
            email=pytest.EMAIL,
            password=pytest.PASSWORD,
        )
    )
    assert response.status_code == 200

def test_validate_auth_token(client, init_database, init_user):
    response = client.get(
        '/validate_token',
        headers=dict(
            Authorization='Bearer ' + init_user.get_auth_token()
        )
    )
    assert response.status_code == 200

def test_fail_validate_wo_auth_token(client, init_database, init_user):
    response = client.get('/validate_token')
    assert response.status_code == 403

@patch(
    "app.model.jwt.decode",
    side_effect=[ExpiredSignatureError()]
)
def test_fail_validate_w_expired_token(mock, client, init_database, init_user):
    response = client.get(
        '/validate_token',
        headers=dict(
            Authorization='Bearer ' + 'expiredtoken'
        )
    )
    assert response.status_code == 401
    assert utils.EXPIRED_SIGNATURE_ERROR in response.get_json().get('message')

@patch(
    "app.model.jwt.decode",
    side_effect=[InvalidTokenError()]
)
def test_fail_validate_w_invalid_token(mock, client, init_database, init_user):
    response = client.get(
        '/validate_token',
        headers=dict(
            Authorization='Bearer ' + 'invalidtoken'
        )
    )
    assert response.status_code == 401
    assert utils.INVALID_TOKEN_ERROR in response.get_json().get('message')

@patch("app.model.User.decode_auth_token")
def test_fail_validate_w_not_exist_user_token(mock, client, init_database, init_user):
    mock.return_value = 'notauuid', True
    response = client.get(
        '/validate_token',
        headers=dict(
            Authorization='Bearer ' + 'goodtoken'
        )
    )
    assert response.status_code == 401
    assert utils.PROVIDE_VALID_TOKEN in response.get_json().get('message')