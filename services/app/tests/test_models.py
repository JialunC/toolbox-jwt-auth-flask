from app.model import User

def test_new_user(client):
    user = User('tom@gmail.com', 'wawaweewa')
    assert user.email == 'tom@gmail.com'
    assert user.password_hash != 'wawaweewa'
