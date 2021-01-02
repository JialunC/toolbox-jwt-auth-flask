from app.model import User

def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'status' in response.get_json()
    assert 'success' in response.get_json().get('status')

def test_create_user(client, init_database):
    EMAIL = 'tom@gmail.com'
    PASSWORD = 'wawaweewa'
    response = client.post(
        '/user',
        json=dict(
            email=EMAIL,
            password=PASSWORD,
        )
    )
    uuid = response.json['uuid']
    user = User.query.filter_by(uuid=uuid).first()
    assert user.email == EMAIL
    assert user.check_password(PASSWORD)
