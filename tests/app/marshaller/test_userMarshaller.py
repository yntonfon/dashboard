from unittest import TestCase

from app.mashaller.user import user_marshaller
from app.model import User


class TestUserMarshaller(TestCase):
    def setUp(self):
        self.payload = {'username': 'pablo', 'email': 'pablo@test.com'}
    
    def test_deserialize_returns_new_user_instanciated_with_the_given_payload(self):
        # When
        actual = user_marshaller.deserialize(self.payload)
        
        # Then
        self.assertIsInstance(actual, User)
    
    def test_deserialize_skips_id_field_if_given(self):
        # Given
        self.payload['id'] = 1
        
        # When
        actual_user = user_marshaller.deserialize(self.payload)
        
        # Then
        self.assertEqual(None, actual_user.id)
    
    def test_deserialize_skips_email_confirmed_field_if_given(self):
        # Given
        self.payload['email_confirmed'] = True
        
        # When
        actual_user = user_marshaller.deserialize(self.payload)
        
        # Then
        self.assertEqual(None, actual_user.email_confirmed)
    
    def test_deserialize_skips_password_hash_field_if_given(self):
        # Given
        self.payload['password_hash'] = 'myhash'
        
        # When
        actual_user = user_marshaller.deserialize(self.payload)
        
        # Then
        self.assertEqual(None, actual_user.password_hash)
    
    def test_serialize_returns_a_user_formatted_as_json(self):
        # Given
        additionnal_fields = {'id': 1, 'email_confirmed': True, 'password_hash': 'myhash'}
        self.payload.update(additionnal_fields)
        users = User(**self.payload)
        
        expected = {
            'email': 'pablo@test.com',
            'email_confirmed': True,
            'id': 1,
            'username': 'pablo'
        }
        
        # When
        actual = user_marshaller.serialize(users)
        
        # Then
        self.assertEqual(expected, actual)
    
    def test_serialize_skips_password_hash_field(self):
        # Given
        additionnal_fields = {'id': 1, 'email_confirmed': True, 'password_hash': 'myhash'}
        self.payload.update(additionnal_fields)
        user = User(**self.payload)
        
        # When
        actual = user_marshaller.serialize(user)
        
        # Then
        self.assertNotIn('password_hash', actual)
    
    def test_serialize_list_returns_a_list_of_user_formatted_as_json(self):
        # Given
        additionnal_fields = {'id': 1, 'email_confirmed': True, 'password_hash': 'myhash'}
        self.payload.update(additionnal_fields)
        users = [User(**self.payload)]
        
        expected = [{
            'email': 'pablo@test.com',
            'email_confirmed': True,
            'id': 1,
            'username': 'pablo'
        }]
        
        # When
        actual = user_marshaller.serialize_list(users)
        
        # Then
        self.assertEqual(expected, actual)
