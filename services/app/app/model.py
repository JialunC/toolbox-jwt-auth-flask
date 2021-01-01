import bcrypt
from datetime import datetime
from app.main import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(255), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.LargeBinary())
    created_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)
        self.created_on = datetime.now()

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def __repr__(self):
        return '<id {}>'.format(self.id)