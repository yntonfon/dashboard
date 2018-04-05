from unittest import TestCase

from marshmallow import ValidationError

from app.validator import user_validator
from .test_utils import TestUtils


class TestUserValidator(TestCase):
    def setUp(self):
        self.payload = {'username': 'pablo', 'email': 'pablo@test.com', 'password': 'mysecret'}
    
    def test_validate_create_payload_raises_error_when_username_is_missing(self):
        # Given
        self.payload.pop('username')
        
        # When
        with self.assertRaises(ValidationError) as error:
            user_validator.validate_create_payload(self.payload)
        
        # Then
        self.assertEqual(TestUtils.MISSING_FIELD, error.exception.messages['username'])
    
    def test_validate_create_payload_raises_error_when_username_is_not_defined(self):
        # Given
        self.payload['username'] = None
        
        # When
        with self.assertRaises(ValidationError) as error:
            user_validator.validate_create_payload(self.payload)
        
        # Then
        self.assertEqual(TestUtils.NULL_FIELD, error.exception.messages['username'])
    
    def test_validate_create_payload_raises_error_when_username_is_empty(self):
        # Given
        self.payload['username'] = ''
        
        # When
        with self.assertRaises(ValidationError) as error:
            user_validator.validate_create_payload(self.payload)
        
        # Then
        self.assertEqual(TestUtils.SHORTER_FIELD, error.exception.messages['username'])
    
    def test_validate_create_payload_raises_error_when_username_is_bad_format(self):
        # Given
        self.payload['username'] = {}
        
        # When
        with self.assertRaises(ValidationError) as error:
            user_validator.validate_create_payload(self.payload)
        
        # Then
        self.assertEqual(TestUtils.NOT_VALID_STRING_FIELD, error.exception.messages['username'])
    
    def test_validate_create_payload_raises_error_when_email_is_missing(self):
        # Given
        self.payload.pop('email')
        
        # When
        with self.assertRaises(ValidationError) as error:
            user_validator.validate_create_payload(self.payload)
        
        # Then
        self.assertEqual(TestUtils.MISSING_FIELD, error.exception.messages['email'])
    
    def test_validate_create_payload_raises_error_when_email_is_not_defined(self):
        # Given
        self.payload['email'] = None
        
        # When
        with self.assertRaises(ValidationError) as error:
            user_validator.validate_create_payload(self.payload)
        
        # Then
        self.assertEqual(TestUtils.NULL_FIELD, error.exception.messages['email'])
    
    def test_validate_create_payload_returns_error_when_email_is_empty(self):
        # Given
        self.payload['email'] = ''
        
        # When
        with self.assertRaises(ValidationError) as error:
            user_validator.validate_create_payload(self.payload)
        
        # Then
        self.assertEqual(TestUtils.NOT_VALID_EMAIL_FIELD, error.exception.messages['email'])
    
    def test_validate_create_payload_raises_error_when_password_is_missing(self):
        # Given
        self.payload.pop('password')
        
        # When
        with self.assertRaises(ValidationError) as error:
            user_validator.validate_create_payload(self.payload)
        
        # Then
        self.assertEqual(TestUtils.MISSING_FIELD, error.exception.messages['password'])
    
    def test_validate_create_payload_raises_error_when_password_is_not_defined(self):
        # Given
        self.payload['password'] = None
        
        # When
        with self.assertRaises(ValidationError) as error:
            user_validator.validate_create_payload(self.payload)
        
        # Then
        self.assertEqual(TestUtils.NULL_FIELD, error.exception.messages['password'])
    
    def test_validate_create_payload_raises_error_when_password_is_empty(self):
        # Given
        self.payload['password'] = ''
        
        # When
        with self.assertRaises(ValidationError) as error:
            user_validator.validate_create_payload(self.payload)
        
        # Then
        self.assertEqual(TestUtils.SHORTER_FIELD, error.exception.messages['password'])
