from unittest import TestCase, mock

from flask import Flask
from flask_bcrypt import Bcrypt

from app.provider.security import SecurityProvider


class TestSecurityProvider(TestCase):
    def setUp(self):
        self.mock_bcrypt = mock.create_autospec(Bcrypt)
        self.mock_app = mock.create_autospec(Flask)
        
        self.security_provider = SecurityProvider(self.mock_app, self.mock_bcrypt)
        
    def test_encrypt_password_generates_hash_of_the_given_password(self):
        # Given
        password = 'mysecret'
        self.mock_app.config = {'BCRYPT_LOG_ROUNDS': 12}
        
        # When
        self.security_provider.encrypt_password(password)
        
        # Then
        self.mock_bcrypt.generate_password_hash.assert_called_with(password, 12)
