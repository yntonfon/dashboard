import json

from app.model import User
from tests.base_test import BaseTest


class TestUserResetPasswordAPI(BaseTest):
    def test_put_sends_an_email_with_link_password_recovery_to_user(self):
        user = User(username='Robert', email='robert@test.com', password_hash='secrethashed', email_confirmed=True)
        self.db.session.add(user)
        self.db.session.commit()
        
        # Given
        data = json.dumps({'email': 'robert@test.com'})
        
        # When
        with self.mail.record_messages() as outbox:
            response = self.client.put('/api/user/reset', data=data, headers={'content-type': 'application/json'})
        
        # Then
        self.assert200(response)
        self.assertEqual(1, len(outbox))
        self.assertIn('robert@test.com', outbox[0].recipients)

    def test_put_returns_404_when_the_user_with_the_given_mail_do_not_exist(self):
        # Given
        user = User(username='Robert', email='robert@test.com', password_hash='secrethashed')
        self.db.session.add(user)
        self.db.session.commit()
        
        bad_data = json.dumps({'email': 'gaspard@test.com'})
        
        # When
        response = self.client.put('/api/user/reset', data=bad_data, headers={'content-type': 'application/json'})
        
        # Then
        self.assert404(response)

    def test_put_returns_400_when_the_user_has_not_yet_confirm_his_email(self):
        # Given
        user = User(username='Robert', email='robert@test.com', password_hash='secrethashed', email_confirmed=False)
        self.db.session.add(user)
        self.db.session.commit()
    
        data = json.dumps({'email': 'robert@test.com'})
    
        # When
        response = self.client.put('/api/user/reset', data=data, headers={'content-type': 'application/json'})
    
        # Then
        self.assert400(response)
