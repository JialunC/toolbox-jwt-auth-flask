EXPIRED_SIGNATURE_ERROR = 'ExpiredSignatureError'
INVALID_TOKEN_ERROR = 'InvalidTokenError'
PROVIDE_VALID_TOKEN = 'Provide a valid auth token.'
ACCOUNT_ALREADY_EXISTS = "Account already exists."

FAILED = 'Failed'
ERROR = 'Error'
SUCCESS = 'Success'

class FormattedResponse(object):
    def __init__(self, status, message=None):
        self.status = status
        if message:
            self.message = message

