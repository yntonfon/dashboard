import json

from app.model import User
from app.provider import security_provider, SaltEnum
from tests.base_test import BaseTest


class TestUserResetPasswordAPI(BaseTest):
    def test_get_resets_user_password_and_send_the_new_password_by_email(self):
        # Given
        user = User(username='Robert', email='robert@test.com', password_hash='secrethashed')
        self.db.session.add(user)
        self.db.session.commit()
        
        token = security_provider.encrypt_to_urlsafetimed('robert@test.com', salt=SaltEnum.reset_password.value)
        
        # When
        with self.mail.record_messages() as outbox:
            response = self.client.get('/api/user/reset?token=%s' % token)
        
        # Then
        self.assertStatus(response, 201)
        self.assertEqual(1, len(outbox))
        self.assertIn('robert@test.com', outbox[0].recipients)
        
        self.db.session.refresh(user)
        self.assertNotEqual('secrethashed', user.password_hash)
    
    def test_get_returns_404_when_user_send_an_invalid_token(self):
        # Given
        user = User(username='Robert', email='robert@test.com', password_hash='secrethashed')
        self.db.session.add(user)
        self.db.session.commit()
        
        bad_token = security_provider.encrypt_to_urlsafetimed('robert@test.com', salt='bad-salt')
        
        # When
        with self.mail.record_messages() as outbox:
            response = self.client.get('/api/user/reset?token=%s' % bad_token)
        
        # Then
        self.assertStatus(response, 404)
    
    def test_get_returns_404_when_user_is_not_found(self):
        # Given
        user = User(username='Robert', email='robert@test.com', password_hash='secrethashed')
        self.db.session.add(user)
        self.db.session.commit()
        
        bad_token = security_provider.encrypt_to_urlsafetimed('INVALID@test.com', salt=SaltEnum.reset_password.value)
        
        # When
        with self.mail.record_messages() as outbox:
            response = self.client.get('/api/user/reset?token=%s' % bad_token)
        
        # Then
        self.assertStatus(response, 404)
    
    def test_put_sends_an_email_with_link_password_recovery_to_user(self):
        # Given
        user = User(username='Robert', email='robert@test.com', password_hash='secrethashed', email_confirmed=True)
        self.db.session.add(user)
        self.db.session.commit()
        
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
