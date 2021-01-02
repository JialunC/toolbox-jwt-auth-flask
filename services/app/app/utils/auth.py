from functools import wraps
from flask import request, jsonify
from app.model import User
from app import utils

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': utils.FAILED,
            'message': utils.PROVIDE_VALID_TOKEN
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(response_object), 403
        auth_token = auth_header.split(" ")[1]
        uuid_or_message, success = User.decode_auth_token(auth_token)
        if not success:
            response_object['message'] = uuid_or_message
            return jsonify(response_object), 401
        user = User.query.filter_by(uuid=uuid_or_message).first()
        if not user:
            return jsonify(response_object), 401
        return f(*args, **kwargs)
    return decorated_function