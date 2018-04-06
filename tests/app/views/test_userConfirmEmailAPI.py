from app.model import User
from app.provider import security_provider, SaltEnum
from tests.base_test import BaseTest


class TestUserConfirmEmailAPI(BaseTest):
    def test_get_confirms_user_email_and_returns_201(self):
        # Given
        user_1 = User(username='user1', email='user1@test.com', password_hash='hash')
        self.db.session.add(user_1)
        self.db.session.commit()
        
        token = security_provider.encrypt_to_urlsafetimed('user1@test.com', salt=SaltEnum.email_confirmation.value)
        
        # When
        response = self.client.get('/api/user/confirm/%s' % token)
        
        # Then
        self.assertStatus(response, 201)
        actual_user = User.query.first()
        self.assertTrue(actual_user.email_confirmed)
    
    def test_get_returns_412_precondition_failed_when_token_is_invalid(self):
        # Given
        user_1 = User(username='user1', email='user1@test.com', password_hash='hash')
        self.db.session.add(user_1)
        self.db.session.commit()
        
        invalid_token = security_provider.encrypt_to_urlsafetimed('user1@test.com', salt='bad-salt')
        
        # When
        response = self.client.get('/api/user/confirm/%s' % invalid_token)
        
        # Then
        self.assertStatus(response, 412)
