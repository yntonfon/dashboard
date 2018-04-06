class UserAlreadyExistException(Exception):
    def __init__(self):
        self.messages = {
            'error_code': 'user-already-exist',
            'description': 'The user seems to be already created. Choose another username or email.'
        }


class UserInvalidTokenException(Exception):
    def __init__(self):
        self.messages = {
            'error_code': 'user-invalid-token',
            'description': 'The token seems to be incorrect. Please request a fresh one.'
        }


class UserNotFoundException(Exception):
    pass
