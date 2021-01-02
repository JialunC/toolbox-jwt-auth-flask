from app.model import User

def test_new_user(client):
    PASSWORD = 'wawaweewa'
    user = User('tom@gmail.com', PASSWORD)
    assert user.email == 'tom@gmail.com'
    assert user.password_hash != PASSWORD
    assert user.check_password(PASSWORD)
    assert not user.check_password('password')
