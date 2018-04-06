from unittest import TestCase, mock

from flask import Flask
from flask_bcrypt import Bcrypt

from app.provider.security import SecurityProvider


class TestSecurityProvider(TestCase):
    def test_encrypt_password_generate_hash_of_given_password(self):
        # Given
        password = 'mysecret'
        mock_app = mock.create_autospec(Flask)
        mock_app.config = {'BCRYPT_LOG_ROUNDS': 12}
        mock_bcrypt = mock.create_autospec(Bcrypt)
        security_provider = SecurityProvider(mock_app, mock_bcrypt)
        
        # When
        security_provider.encrypt_password(password)
        
        # Then
        mock_bcrypt.generate_password_hash.assert_called_with(password, 12)
