from unittest import TestCase
from unittest.mock import Mock

from app.provider.url import UrlProvider


class TestUrlProvider(TestCase):
    def test_build_url_from_returns_generates_api_url_based_on_the_given_api_and_data(self):
        # Given
        api = 'myAPI'
        external_link = True
        token = 'cooltoken'
        mock_url_for = Mock()
        
        provider = UrlProvider(mock_url_for)
        
        # When
        provider.create_url_for(api, external_link, token=token)
        
        # Then
        mock_url_for.assert_called_with('myAPI', _external=True, token=token)

    def test_build_url_from_returns_generated_url(self):
        # Given
        api = 'myAPI'
        external_link = True
        token = 'cooltoken'
        mock_url_for = Mock(return_value='newurl')
        
        provider = UrlProvider(mock_url_for)
        
        # When
        actual = provider.create_url_for(api, external_link, token=token)
        
        # Then
        self.assertEqual('newurl', actual)
