from itsdangerous import URLSafeTimedSerializer

from app.extension import bcrypt as bcrypt_instance


class SecurityProvider:
    EMAIL_CONFIRMATION_LINK_KEY = 'email-confirmation-link'
    
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

    def build_url_safe_timed(self, token, salt):
        return self.urlsafetimed_serializer.dumps(token, salt=salt)
        

security_provider = SecurityProvider(bcrypt_instance, URLSafeTimedSerializer)
