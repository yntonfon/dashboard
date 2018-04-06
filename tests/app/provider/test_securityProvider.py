from unittest import TestCase, mock
from unittest.mock import Mock

from flask import Flask
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer

from app.provider.security import SecurityProvider


class TestSecurityProvider(TestCase):
    def setUp(self):
        self.mock_bcrypt = mock.create_autospec(Bcrypt)
        self.mock_app = mock.create_autospec(Flask)
        self.mock_url_safe_timed_serializer = mock.create_autospec(URLSafeTimedSerializer)
        
        self.security_provider = SecurityProvider(self.mock_app, self.mock_bcrypt, self.mock_url_safe_timed_serializer)
        
    def test_encrypt_password_generates_hash_of_the_given_password(self):
        # Given
        password = 'mysecret'
        self.mock_app.config = {'BCRYPT_LOG_ROUNDS': 12}
        
        # When
        self.security_provider.encrypt_password(password)
        
        # Then
        self.mock_bcrypt.generate_password_hash.assert_called_with(password, 12)

    def test_build_url_safe_timed_token_instanciates_serializer_class_with_secret_key(self):
        # Given
        token = 'stringtosafe'
        self.mock_app.config = {'SECRET_KEY': 'uhooh'}
        
        # When
        self.security_provider.build_url_safe_timed_token(token, salt='salt')
        
        # Then
        self.mock_url_safe_timed_serializer.assert_called_with('uhooh')

    def test_build_url_safe_timed_token_generates_URL_safe_string_with_time_information(self):
        # Given
        token = 'stringtosafe'
        serialize = Mock()
        self.mock_app.config = {'SECRET_KEY': 'uhooh'}
        self.mock_url_safe_timed_serializer.return_value = serialize
        
        # When
        self.security_provider.build_url_safe_timed_token(token, salt='salt')
        
        # Then
        serialize.dumps.assert_called_with(token, salt='salt')
