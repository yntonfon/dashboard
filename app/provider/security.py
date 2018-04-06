from flask import current_app
from itsdangerous import URLSafeTimedSerializer

from app.extension import bcrypt


class SecurityProvider:
    def __init__(self, app, bcrypt, urlsafetimedserializer_cls):
        self.app = app
        self.bcrypt = bcrypt
        self.urlsafetimedserializer_cls = urlsafetimedserializer_cls
    
    def encrypt_password(self, password):
        return self.bcrypt.generate_password_hash(password, self.app.config['BCRYPT_LOG_ROUNDS'])

    def build_url_safe_timed_token(self, token, salt):
        serializer = self.urlsafetimedserializer_cls(self.app.config['SECRET_KEY'])
        return serializer.dumps(token, salt=salt)
        

security_provider = SecurityProvider(current_app, bcrypt, URLSafeTimedSerializer)
