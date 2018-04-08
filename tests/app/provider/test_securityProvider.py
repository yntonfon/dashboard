from unittest import TestCase, mock

from flask import Flask
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer, BadData

from app.exception import InvalidTokenException
from app.provider.security import SecurityProvider


class TestSecurityProvider(TestCase):
    def setUp(self):
        self.mock_bcrypt = mock.create_autospec(Bcrypt)
        self.mock_app = mock.create_autospec(Flask)
        self.mock_urlsafetimed_serializer = mock.create_autospec(URLSafeTimedSerializer)
        self.provider = SecurityProvider(self.mock_bcrypt, self.mock_urlsafetimed_serializer)

        self.mock_app.config = {'SECRET_KEY': 'mysecret', 'BCRYPT_LOG_ROUNDS': 12, 'URL_SAFE_TIMED_MAX_AGE': 1}
        
    def test_init_app_sets_app(self):
        # When
        self.provider.init_app(self.mock_app)
        
        # Then
        self.assertEqual(self.mock_app, self.provider.app)

    def test_init_app_instanciates_new_uURL_SAFE_TIMED_MAX_AGErlsafetimed_serializer(self):
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

    def test_encrypt_to_urlsafetimed_serializes_data_to_URL_safe_token_with_time_information(self):
        # Given
        data = 'datatosecure'
        salt = 'mysalt'
        self.provider.urlsafetimed_serializer = self.mock_urlsafetimed_serializer
        
        # When
        self.provider.encrypt_to_urlsafetimed(data, salt=salt)
        
        # Then
        self.mock_urlsafetimed_serializer.dumps.assert_called_with(data, salt=salt)

    def test_decrypt_from_urlsafetimed_deserializes_token_to_original_data(self):
        # Given
        token = 'tokentodeserialize'
        salt = 'mysalt'
        self.provider.app = self.mock_app
        self.provider.urlsafetimed_serializer = self.mock_urlsafetimed_serializer
    
        # When
        self.provider.decrypt_from_urlsafetimed(token, salt=salt)
    
        # Then
        self.mock_urlsafetimed_serializer.loads.assert_called_with(token, salt=salt, max_age=1)

    def test_decrypt_from_urlsafetimed_raises_when_token_is_invalid(self):
        # Given
        token = 'tokentodeserialize'
        salt = 'mysalt'
        self.mock_urlsafetimed_serializer.loads.side_effect = BadData('')
        self.provider.app = self.mock_app
        self.provider.urlsafetimed_serializer = self.mock_urlsafetimed_serializer
    
        # When
        with self.assertRaises(InvalidTokenException):
            self.provider.decrypt_from_urlsafetimed(token, salt=salt)

    def test_generate_password_returns_a_new_password(self):
        # When
        actual = self.provider.generate_password()
    
        # Then
        self.assertEqual('Password01!', actual)
