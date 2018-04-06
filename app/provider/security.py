from enum import Enum

from itsdangerous import URLSafeTimedSerializer

from app.extension import bcrypt as bcrypt_instance


class Salt(Enum):
    email_confirmation = 'email-confirmation-salt'


class SecurityProvider:
    def __init__(self, bcrypt, urlsafetimed_serializer_cls):
        self.bcrypt = bcrypt
        self._urlsafetimed_serializer_cls = urlsafetimed_serializer_cls
        self.urlsafetimed_serializer = None
        self.app = None
    
    def init_app(self, app):
        self.app = app
        self.urlsafetimed_serializer = self._urlsafetimed_serializer_cls(app.config['SECRET_KEY'])
    
    def encrypt_password(self, password):
        return self.bcrypt.generate_password_hash(password, self.app.config['BCRYPT_LOG_ROUNDS'])
    
    def encrypt_to_urlsafetimed(self, token, salt):
        return self.urlsafetimed_serializer.dumps(token, salt=salt)


security_provider = SecurityProvider(bcrypt_instance, URLSafeTimedSerializer)
