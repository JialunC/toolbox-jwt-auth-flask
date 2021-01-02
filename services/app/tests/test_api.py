import pytest
from app.model import User

def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'status' in response.get_json()
    assert 'success' in response.get_json().get('status')

def test_create_user(client, init_database):
    response = client.post(
        '/user',
        json=dict(
            email=pytest.EMAIL,
            password=pytest.PASSWORD,
        )
    )
    uuid = response.json['uuid']
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
    assert 'error' in response.get_json().get('status')
    assert 'acount already exists' in response.get_json().get('message')

def test_auth(client, init_database, init_user):
    response = client.post(
        '/auth',
        json=dict(
            email=pytest.EMAIL,
            password=pytest.PASSWORD,
        )
    )
    assert response.status_code == 200

