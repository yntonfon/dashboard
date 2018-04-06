from unittest import TestCase, mock
from unittest.mock import Mock

from sqlalchemy.exc import IntegrityError

from app.controller.user import UserController
from app.exception.user import UserAlreadyExistException
from app.mashaller.user import UserMarshaller
from app.provider.security import SecurityProvider
from app.repository.user import UserRepository


class TestUserController(TestCase):
    def setUp(self):
        self.user_repository = mock.create_autospec(UserRepository)
        self.user_marshaller = mock.create_autospec(UserMarshaller)
        self.security_provider = mock.create_autospec(SecurityProvider)
        self.controller = UserController(self.user_repository, self.user_marshaller, self.security_provider)
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
            'description': 'The user seems to be already created. Choose another username or email'
        }
        
        # When
        with self.assertRaises(UserAlreadyExistException) as error:
            self.controller.create_user(self.payload)
        
        self.assertEqual(expected, error.exception.messages)
