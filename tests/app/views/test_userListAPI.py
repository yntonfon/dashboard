import json

from app.model import User
from tests.base_test import BaseTest


class TestUserListAPI(BaseTest):
    def test_get_returns_200_with_all_users_list(self):
        # Given
        user_1 = User(username='user1', email='user1@test.com', password_hash='hash')
        user_2 = User(username='user2', email='user2@test.com', password_hash='hash')
        self.db.session.add(user_1)
        self.db.session.add(user_2)
        self.db.session.commit()
        
        expected = [
            {
                'id': 1,
                'username': 'user1',
                'email': 'user1@test.com',
                'email_confirmed': False
            },
            {
                'id': 2,
                'username': 'user2',
                'email': 'user2@test.com',
                'email_confirmed': False
            }
        ]
        
        # When
        response = self.client.get('/api/users')
        
        # Then
        self.assert200(response)
        self.assertEqual(expected, response.json)
    
    def test_post_creates_a_new_user_and_returns_200_with_the_new_user_id(self):
        # Given
        user = json.dumps({
            'username': 'thomas',
            'email': 'thomas@test.com',
            'password': 'gaspard'
        })
        
        expected_data = {'id': 1}
        
        # When
        response = self.client.post('/api/users', data=user, headers={'content-type': 'application/json'})
        
        # Then
        self.assert200(response)
        self.assertEqual(expected_data, response.json)
        
        actual_user = User.query.first()
        self.assertEqual(1, actual_user.id)
        self.assertEqual('thomas', actual_user.username)
        self.assertEqual('thomas@test.com', actual_user.email)
        self.assertEqual(False, actual_user.email_confirmed)
        self.assertIsNotNone(actual_user.password_hash)
    
    def test_post_sends_an_email_to_the_new_created_user(self):
        # Given
        user = json.dumps({
            'username': 'thomas',
            'email': 'thomas@test.com',
            'password': 'gaspard'
        })
        
        # When
        with self.mail.record_messages() as outbox:
            response = self.client.post('/api/users', data=user, headers={'content-type': 'application/json'})
        
        # Then
        self.assert200(response)
        self.assertEqual(1, len(outbox))
        self.assertIn('thomas@test.com', outbox[0].recipients)
        
    def test_post_returns_400_when_user_informations_are_invalid(self):
        # Given
        user = json.dumps({
            'email': 'user1@@@test.com',
            "password": ''
        })
        
        expected = {
            'username': ['Missing data for required field.'],
            'password': ['Shorter than minimum length 1.'],
            'email': ['Not a valid email address.']
        }
        
        # When
        response = self.client.post('/api/users', data=user, headers={'content-type': 'application/json'})
        
        # Then
        self.assert400(response)
        self.assertEqual(expected, response.json)
    
    def test_post_returns_422_when_a_user_already_exists(self):
        # Given
        user_1 = User(username='thomas', email='thomas@test.com', password_hash='myhash')
        self.db.session.add(user_1)
        self.db.session.commit()
        
        user_to_create = json.dumps({
            'username': 'thomas',
            'email': 'thomas@test.com',
            "password": 'mysecret'
        })
        
        # When
        response = self.client.post('/api/users', data=user_to_create, headers={'content-type': 'application/json'})
        
        # Then
        self.assertStatus(response, 422)
