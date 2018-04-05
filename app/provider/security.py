from flask import current_app

from . import bcrypt


class Security:
    def __init__(self, app, bcrypt):
        self.app = app
        self.bcrypt = bcrypt
    
    def encrypt_password(self, password):
        return self.bcrypt.generate_password_hash(password, self.app.config['BCRYPT_LOG_ROUNDS'])


security = Security(current_app, bcrypt)
