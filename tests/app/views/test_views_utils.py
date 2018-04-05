from unittest.mock import Mock

from app.views import handle_views_exception
from tests.base_test import BaseTest


class TestHandleViewsException(BaseTest):
    def test_sets_status_code_on_response_from_error(self):
        # Given
        error = Mock()
        error_payload = {'field': 'error message'}
        error.to_dict.return_value = error_payload
        error.configure_mock(status_code=400)
        
        # When
        response = handle_views_exception(error)
        
        # Then
        assert 400 == response.status_code
        assert error_payload == response.json
