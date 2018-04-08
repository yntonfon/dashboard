from unittest import TestCase

from app.domain import UserDomain
from app.model import User


class TestUserDomain(TestCase):
    def test_is_active_return_true_when_email_is_confirmed(self):
        # Given
        domain = UserDomain()
        user = User(email_confirmed=True)
        expected = True
        
        # When
        actual = domain.is_active(user)
        
        # Then
        self.assertEqual(expected, actual)
    
    def test_is_active_return_false_when_email_is_not_confirmed(self):
        # Given
        domain = UserDomain()
        user = User(email_confirmed=False)
        expected = False
        
        # When
        actual = domain.is_active(user)
        
        # Then
        self.assertEqual(expected, actual)
