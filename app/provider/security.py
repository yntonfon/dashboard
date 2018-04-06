from flask import current_app

from app.extension import bcrypt


class SecurityProvider:
    def __init__(self, app, bcrypt):
        self.app = app
        self.bcrypt = bcrypt
    
    def encrypt_password(self, password):
        return self.bcrypt.generate_password_hash(password, self.app.config['BCRYPT_LOG_ROUNDS'])


security_provider = SecurityProvider(current_app, bcrypt)
