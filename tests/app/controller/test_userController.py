from unittest import TestCase, mock
from unittest.mock import Mock

from sqlalchemy.exc import IntegrityError

from app.controller.user import UserController
from app.domain import UserDomain
from app.exception import (UserAlreadyExistException, UserInvalidTokenException, UserNotFoundException,
                           InvalidTokenException, UserNotActiveException)
from app.mashaller.user import UserMarshaller
from app.provider.security import SecurityProvider
from app.repository.user import UserRepository


class TestUserController(TestCase):
    def setUp(self):
        self.user_repository = mock.create_autospec(UserRepository)
        self.user_marshaller = mock.create_autospec(UserMarshaller)
        self.security_provider = mock.create_autospec(SecurityProvider)
        self.user_domain = mock.create_autospec(UserDomain)
        self.controller = UserController(self.user_repository, self.user_marshaller, self.security_provider,
                                         self.user_domain)
        
        self.payload = {'username': 'pablo', 'email': 'pablo@test.com', 'password': 'rawpassword'}
    
    def test_get_users_returns_all_user_list(self):
        # Given
        self.user_repository.get_all.return_value = 'allusers'
        
        # When
        actual = self.controller.get_users()
        
        # Then
        self.assertEqual('allusers', actual)
    
    def test_create_user_deserializes_the_given_payload(self):
        # When
        self.controller.create_user(self.payload)
        
        # Then
        self.user_marshaller.deserialize.assert_called_with(self.payload)
    
    def test_create_user_sets_user_password_field_with_hash_of_the_given_password(self):
        # Given
        user = Mock()
        hashed_password = 'myhashpassword'
        self.user_marshaller.deserialize.return_value = user
        self.security_provider.encrypt_password.return_value = hashed_password
        
        # When
        self.controller.create_user(self.payload)
        
        # Then
        self.assertEqual(user.password_hash, hashed_password)
    
    def test_create_user_save_the_new_user(self):
        # Given
        user = Mock()
        self.user_marshaller.deserialize.return_value = user
        
        # When
        self.controller.create_user(self.payload)
        
        # Then
        self.user_repository.save.assert_called_with(user)
    
    def test_create_user_returns_the_new_user_id(self):
        # Given
        user_id = 'userid'
        self.user_repository.save.return_value = user_id
        
        expected = {'id': user_id}
        
        # When
        actual = self.controller.create_user(self.payload)
        
        # Then
        self.assertEqual(expected, actual)
    
    def test_create_user_raises_error_when_user_already_exist(self):
        # Given
        self.user_repository.save.side_effect = IntegrityError(statement=None, params=None, orig=None)
        
        expected = {
            'error_code': 'user-already-exist',
            'description': 'The user seems to be already created. Choose another username or email.'
        }
        
        # When
        with self.assertRaises(UserAlreadyExistException) as error:
            self.controller.create_user(self.payload)
        
        self.assertEqual(expected, error.exception.messages)

    def test_confirm_email_deserializes_given_token_with_appropriate_salt_and_max_age(self):
        # Given
        token = 'token'

        # When
        self.controller.confirm_email(token)

        # Then
        self.security_provider.decrypt_from_urlsafetimed.assert_called_with(token, salt='email-confirmation-salt')

    def test_confirm_email_fetchs_user_by_email(self):
        # Given
        token = 'token'
        email = 'myemail'
        self.security_provider.decrypt_from_urlsafetimed.return_value = email

        # When
        self.controller.confirm_email(token)

        # Then
        self.user_repository.get_by.assert_called_with(email=email)

    def test_confirm_email_sets_user_email_confirmed_field_to_true(self):
        # Given
        token = 'token'
        user = Mock()
        self.user_repository.get_by.return_value = user

        # When
        self.controller.confirm_email(token)

        # Then
        self.assertEqual(True, user.email_confirmed)

    def test_confirm_email_saves_user_modification(self):
        # Given
        token = 'token'
        user = Mock()
        self.user_repository.get_by.return_value = user

        # When
        self.controller.confirm_email(token)

        # Then
        self.user_repository.save.assert_called_with(user)

    def test_confirm_email_raises_when_token_is_invalid(self):
        # Given
        token = 'token'
        self.security_provider.decrypt_from_urlsafetimed.side_effect = InvalidTokenException()

        expected = {
            'error_code': 'user-invalid-token',
            'description': 'The token seems to be incorrect. Please request a fresh one.'
        }

        # When
        with self.assertRaises(UserInvalidTokenException) as error:
            self.controller.confirm_email(token)

        # Then
        self.assertEqual(expected, error.exception.messages)

    def test_confirm_email_raises_when_user_is_not_found(self):
        # Given
        token = 'token'
        self.user_repository.get_by.side_effect = UserNotFoundException()

        expected = {
            'error_code': 'user-invalid-token',
            'description': 'The token seems to be incorrect. Please request a fresh one.'
        }

        # When
        with self.assertRaises(UserInvalidTokenException) as error:
            self.controller.confirm_email(token)

        # Then
        self.assertEqual(expected, error.exception.messages)

    def test_get_user_fetchs_user_from_repository(self):
        # Given
        email = 'foo@test.com'

        # When
        self.controller.get_user(email)

        # Then
        self.user_repository.get_by.assert_called_with(email=email)

    def test_validate_user_status_raises_when_email_is_not_confirmed(self):
        # Given
        user = 'user'
        self.user_domain.is_active.return_value = False
    
        expected = {
            'error_code': 'user-not-active',
            'description': 'Your email is not confirmed. Please consider to confirm your email first'
        }
    
        # When
        with self.assertRaises(UserNotActiveException) as error:
            self.controller.validate_user_status(user)
    
        self.assertEqual(expected, error.exception.messages)

    def test_reset_password_deserializes_urlsafetimed_token(self):
        # Given
        token = 'token'
    
        # When
        self.controller.reset_password(token)
    
        # Then
        self.security_provider.decrypt_from_urlsafetimed.assert_called_with(token, salt='reset-password-salt')

    def test_reset_password_fetchs_user_by_the_email_containing_in_the_token(self):
        # Given
        token = 'token'
        email = 'email'
        self.security_provider.decrypt_from_urlsafetimed.return_value = 'email'
    
        # When
        self.controller.reset_password(token)
    
        # Then
        self.user_repository.get_by.assert_called_with(email=email)

    def test_reset_password_generates_a_brand_new_password(self):
        # Given
        token = 'token'
    
        # When
        self.controller.reset_password(token)
    
        # Then
        self.security_provider.generate_password.assert_called_with()

    def test_reset_password_hashes_the_new_password(self):
        # Given
        token = 'token'
        rawpassword = 'rawpassword'
        self.security_provider.generate_password.return_value = rawpassword
    
        # When
        self.controller.reset_password(token)
    
        # Then
        self.security_provider.encrypt_password.assert_called_with(rawpassword)

    def test_reset_password_sets_new_encrypted_password_to_user(self):
        # Given
        token = 'token'
        user = Mock()
        encryptedpassword = 'encryptedpassword'
        self.user_repository.get_by.return_value = user
        self.security_provider.encrypt_password.return_value = encryptedpassword
    
        # When
        self.controller.reset_password(token)
    
        # Then
        self.assertEqual(encryptedpassword, user.password_hash)

    def test_reset_password_saves_modification_on_user(self):
        # Given
        token = 'token'
        user = Mock()
        self.user_repository.get_by.return_value = user
    
        # When
        self.controller.reset_password(token)
    
        # Then
        self.user_repository.save.assert_called_with(user)

    def test_reset_password_returns_email_and_then_new_password_non_encrypted(self):
        # Given
        token = 'token'
        email = 'email'
        rawpassword = 'rawpassword'
        self.security_provider.decrypt_from_urlsafetimed.return_value = email
        self.security_provider.generate_password.return_value = rawpassword
    
        expected = {'email': email, 'password': rawpassword}
    
        # When
        actual = self.controller.reset_password(token)
    
        # Then
        self.assertEqual(expected, actual)

    def test_reset_password_raises_when_token_is_invalid(self):
        # Given
        token = 'token'
        self.security_provider.decrypt_from_urlsafetimed.side_effect = InvalidTokenException()
    
        expected = {
            'error_code': 'user-invalid-token',
            'description': 'The token seems to be incorrect. Please request a fresh one.'
        }
    
        # When
        with self.assertRaises(UserInvalidTokenException) as error:
            self.controller.reset_password(token)
    
        # Then
        self.assertEqual(expected, error.exception.messages)

    def test_reset_password_raises_when_user_is_not_found(self):
        # Given
        token = 'token'
        self.user_repository.get_by.side_effect = UserNotFoundException()
    
        expected = {
            'error_code': 'user-invalid-token',
            'description': 'The token seems to be incorrect. Please request a fresh one.'
        }
    
        # When
        with self.assertRaises(UserInvalidTokenException) as error:
            self.controller.reset_password(token)
    
        # Then
        self.assertEqual(expected, error.exception.messages)
