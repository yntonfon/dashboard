from enum import Enum

from itsdangerous import URLSafeTimedSerializer, BadData

from app.exception import InvalidTokenException
from app.extension import bcrypt as bcrypt_instance


class SaltEnum(Enum):
    email_confirmation = 'email-confirmation-salt'
    reset_password = 'reset-password-salt'


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

    def generate_password(self):
        return 'Password01!'

    def encrypt_to_urlsafetimed(self, data, salt):
        return self.urlsafetimed_serializer.dumps(data, salt=salt)

    def decrypt_from_urlsafetimed(self, token, salt):
        try:
            return self.urlsafetimed_serializer.loads(token, salt=salt,
                                                      max_age=self.app.config['URL_SAFE_TIMED_MAX_AGE'])
        except BadData:
            raise InvalidTokenException()


security_provider = SecurityProvider(bcrypt_instance, URLSafeTimedSerializer)
