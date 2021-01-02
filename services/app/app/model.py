import bcrypt
import jwt
import uuid
from datetime import datetime, timedelta
from app.main import db
from flask import current_app

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(255), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.LargeBinary())
    created_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, password):
        self.email = email
        self.uuid = uuid.uuid4()
        self.set_password(password)
        self.created_on = datetime.now()

    def set_password(self, password):
        salt_round = current_app.config.get('SALT_ROUND')
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(salt_round))

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
    
    def get_auth_token(self):
        payload = {
            'exp': datetime.utcnow() + timedelta(
                minutes=current_app.config.get('JWT_LIFE_MIN')
            ),
            'iat': datetime.utcnow(),
            'sub': self.uuid
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm=current_app.config.get('JWT_SIGNING'),
        )
    
    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token,
                current_app.config.get('SECRET_KEY'),
                algorithms=current_app.config.get('JWT_SIGNING')
            )
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'ExpiredSignatureError'
        except jwt.InvalidTokenError:
            return 'InvalidTokenError'


    def __repr__(self):
        return '<id {}>'.format(self.id)