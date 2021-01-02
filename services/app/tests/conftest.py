import pytest

from app.main import create_app, db

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