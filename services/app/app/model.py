from main import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.LargeBinary())

    def __init__(self, email):
        self.email = email

    def set_password(self, password):
        pass

    def check_password(self, password):
        pass

    def __repr__(self):
        return '<id {}>'.format(self.id)