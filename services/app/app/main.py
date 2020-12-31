import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
PORT = os.getenv('PORT')

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def ping_pong():
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)