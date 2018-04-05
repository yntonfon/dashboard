from app.model import User
from app.repository import user_repository
from tests.base_test import BaseTest


class TestUserRepository(BaseTest):
    def test_save_returns_user_id(self):
        # Given
        user_1 = User(username='user1', email='user1@test.com', password_hash='hash')
        
        # When
        actual = user_repository.save(user_1)
        
        # Then
        self.assertEqual(1, actual)
