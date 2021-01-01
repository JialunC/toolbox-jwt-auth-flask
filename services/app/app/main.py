import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    @app.route('/', methods=['GET'])
    def ping_pong():
        return jsonify({'status': 'success'})

    return app