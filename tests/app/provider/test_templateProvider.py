from unittest import TestCase
from unittest.mock import Mock

from app.provider.template import TemplateProvider


class TestTemplateProvider(TestCase):
    def test_render_template_generates_the_given_template_formatted_with_the_given_data(self):
        # Given
        template = 'mytemplate'
        data = 'mydatatoformat'
        mock_render_template_engine = Mock()
        provider = TemplateProvider(mock_render_template_engine)
        
        # When
        provider.render_template(template, data=data)
        
        # Then
        mock_render_template_engine.assert_called_with(template, data=data)

    def test_render_template_returns_the_generated_template(self):
        # Given
        template = 'mytemplate'
        data = 'mydatatoformat'
        mock_render_template_engine = Mock(return_value='generatedtemplate')
        provider = TemplateProvider(mock_render_template_engine)
        
        # When
        actual = provider.render_template(template, data=data)
        
        # Then
        self.assertEqual('generatedtemplate', actual)
