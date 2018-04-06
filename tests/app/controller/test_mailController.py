from unittest import TestCase, mock

from app.controller.mail import MailController
from app.provider.mail import MailProvider, MsgTemplate
from app.provider.security import SecurityProvider
from app.provider.template import TemplateProvider
from app.provider.url import UrlProvider


class TestMailController(TestCase):
    def setUp(self):
        self.email = 'amnesty@test.com'
        self.security_provider = mock.create_autospec(SecurityProvider)
        self.url_provider = mock.create_autospec(UrlProvider)
        self.template_provider = mock.create_autospec(TemplateProvider)
        self.mail_provider = mock.create_autospec(MailProvider)
        self.controller = MailController(self.security_provider,
                                         self.url_provider,
                                         self.template_provider,
                                         self.mail_provider)
    
    def test_send_confirmation_email_link_generates_safe_token_from_the_given_email(self):
        # When
        self.controller.send_confirmation_email_link(self.email)
        
        # Then
        self.security_provider.build_url_safe_timed.assert_called_with(self.email, salt='email-confirmation-link')
    
    def test_send_confirmation_email_link_generates_confirmation_url_with_the_token(self):
        # Given
        token = 'nicetoken'
        self.security_provider.build_url_safe_timed.return_value = token
        
        # When
        self.controller.send_confirmation_email_link(self.email)
        
        # Then
        self.url_provider.build_url_from.assert_called_with('ConfirmationEmailAPI', external=True, token=token)
    
    def test_send_confirmation_email_link_generates_email_template_containing_url(self):
        # Given
        url = 'niceurl'
        self.url_provider.build_url_from.return_value = url
        
        # When
        self.controller.send_confirmation_email_link(self.email)
        
        # Then
        self.template_provider.render_template.assert_called_with('email/activate.html', confirm_url=url)
    
    def test_send_confirmation_email_link_sends_email_with_template_to_the_given_address(self):
        # Given
        email_content = 'emailcontent'
        self.template_provider.render_template.return_value = email_content
        
        expected = MsgTemplate(
            subject='Confirm your email',
            html=email_content,
            recipients=[self.email]
        )
        
        # When
        self.controller.send_confirmation_email_link(self.email)
        
        # Then
        self.mail_provider.send.assert_called_with(expected)
