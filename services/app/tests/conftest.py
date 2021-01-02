import pytest
from app.main import create_app, db
from app.model import User

def pytest_configure():
    pytest.EMAIL = 'tom@gmail.com'
    pytest.PASSWORD = 'wawaweewa'
    pytest.NEW_EMAIL = 'tomnew@gmail.com'
    pytest.NEW_PASSWORD = 'newwawaweewa'

@pytest.fixture
def client():
    app = create_app('app.config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def init_database(client):
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()

@pytest.fixture
def init_user(client):
    user = User(pytest.EMAIL, pytest.PASSWORD)
    db.session.add(user)
    db.session.commit()
    return user