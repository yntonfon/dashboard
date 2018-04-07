from app.model import User
from tests.base_test import BaseTest


class TestUserResetPasswordAPI(BaseTest):
    def test_put_resets_the_user_password_and_send_him_an_email(self):
        # Given
        user = User(username='Robert', email='robert@test.com', password_hash='secrethashed')
        self.db.session.add(user)
        self.db.session.commit()
        
        email = 'robert@test.com'
        
        # When
        with self.mail.record_messages() as outbox:
            response = self.client.post('/user/reset', data=email, headers={'content-type': 'application/json'})
        
        # Then
        self.assert200(response)
        self.db.session.refresh(user)
        self.assertNotEqual('secrethashed', user.password_hash)
        self.assertEqual(1, len(outbox))
        self.assertEqual('robert@test.com', outbox[0].recipients)
