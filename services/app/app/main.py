import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
db = SQLAlchemy()
from app.model import User

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def ping_pong():
        return jsonify({'status': 'success'})
    
    @app.route('/user', methods=['POST'])
    def add_user():
        data = request.get_json()
        user = User(**data)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': 'acount already exists'
            }), 404
        return jsonify({'uuid': user.uuid}), 201

    @app.route('/auth', methods=['POST'])
    def auth_user():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user.check_password(data['password']):
            auth_token = user.get_auth_token()
            return jsonify({'token': auth_token})
        return jsonify({'status': 'error'})

    return app