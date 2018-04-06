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
        self.mock_urlsafetimed_serializer = mock.create_autospec(URLSafeTimedSerializer)
        self.provider = SecurityProvider(self.mock_bcrypt, self.mock_urlsafetimed_serializer)
        
        self.mock_app.config = {'SECRET_KEY': 'mysecret', 'BCRYPT_LOG_ROUNDS': 12}
        
    def test_init_app_sets_app(self):
        # When
        self.provider.init_app(self.mock_app)
        
        # Then
        self.assertEqual(self.mock_app, self.provider.app)
        
    def test_init_app_instanciates_new_urlsafetimed_serializer(self):
        # When
        self.provider.init_app(self.mock_app)
        
        # Then
        self.mock_urlsafetimed_serializer.assert_called_with('mysecret')
        
    def test_init_app_sets_new_urlsafetimed_serializer(self):
        # Given
        self.mock_urlsafetimed_serializer.return_value = 'serializer'
        
        # When
        self.provider.init_app(self.mock_app)
        
        # Then
        self.assertEqual('serializer', self.provider.urlsafetimed_serializer)
    
    def test_encrypt_password_generates_hash_of_the_given_password(self):
        # Given
        password = 'mysecret'
        self.provider.app = self.mock_app
        
        # When
        self.provider.encrypt_password(password)
        
        # Then
        self.mock_bcrypt.generate_password_hash.assert_called_with(password, 12)

    def test_build_url_safe_timed_generates_URL_safe_string_with_time_information(self):
        # Given
        data = 'datatosecure'
        salt = 'mysalt'
        self.provider.urlsafetimed_serializer = self.mock_urlsafetimed_serializer
        
        # When
        self.provider.build_url_safe_timed(data, salt=salt)
        
        # Then
        self.mock_urlsafetimed_serializer.dumps.assert_called_with(data, salt=salt)
