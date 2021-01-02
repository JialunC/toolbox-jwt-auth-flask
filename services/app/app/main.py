import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
db = SQLAlchemy()
from app.model import User
from app import utils
from app.utils.auth import authenticate

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def ping_pong():
        return jsonify(
            utils.FormattedResponse(utils.SUCCESS).__dict__
        )
    
    @app.route('/user', methods=['POST'])
    def add_user():
        data = request.get_json()
        user = User(**data)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify(
                utils.FormattedResponse(
                    utils.ERROR, utils.ACCOUNT_ALREADY_EXISTS
                ).__dict__
            ), 404
        return jsonify(
            utils.FormattedResponse(
                utils.SUCCESS, {'uuid': user.uuid}
            ).__dict__
        ), 201

    @app.route('/auth', methods=['POST'])
    def auth_user():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            auth_token = user.get_auth_token()
            return jsonify(
                utils.FormattedResponse(
                    utils.ERROR,
                    {'token': auth_token}
                ).__dict__
            )
        return jsonify(
            utils.FormattedResponse(utils.ERROR).__dict__
        ), 404
    
    @app.route('/validate_token', methods=['GET'])
    @authenticate
    def validate_token():
        return jsonify(
            utils.FormattedResponse(utils.SUCCESS).__dict__
        )

    return app