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

    def test_send_confirmation_link_serializes_given_email_as_url_safe_timed_token(self):
        # When
        self.controller.send_confirmation_link(self.email)
        
        # Then
        self.security_provider.encrypt_to_urlsafetimed.assert_called_with(self.email, salt='email-confirmation-salt')

    def test_send_confirmation_link_creates_secure_link_with_the_token(self):
        # Given
        token = 'nicetoken'
        self.security_provider.encrypt_to_urlsafetimed.return_value = token
        
        # When
        self.controller.send_confirmation_link(self.email)
        
        # Then
        self.url_provider.create_url_for.assert_called_with('user.user_confirm', external=True, token=token)

    def test_send_confirmation_link_creates_email_body_containing_the_reset_link(self):
        # Given
        url = 'niceurl'
        self.url_provider.create_url_for.return_value = url
        
        # When
        self.controller.send_confirmation_link(self.email)
        
        # Then
        self.template_provider.render_template.assert_called_with('email/activate.html', confirm_url=url)

    def test_send_confirmation_link_sends_email_to_the_given_address(self):
        # Given
        email_content = 'emailcontent'
        self.template_provider.render_template.return_value = email_content
        
        expected = MsgTemplate(
            subject='Confirm your email',
            html=email_content,
            recipients=[self.email]
        )
        
        # When
        self.controller.send_confirmation_link(self.email)
        
        # Then
        self.mail_provider.send.assert_called_with(expected)

    def test_send_reset_password_link_serializes_given_email_as_url_safe_timed_token(self):
        # When
        self.controller.send_reset_password_link(self.email)
    
        # Then
        self.security_provider.encrypt_to_urlsafetimed.assert_called_with(self.email, salt='reset-password-salt')

    def test_send_reset_password_link_creates_secure_link_to_reset_password(self):
        # Given
        token = 'token'
        self.security_provider.encrypt_to_urlsafetimed.return_value = token
    
        # When
        self.controller.send_reset_password_link(self.email)
    
        # Then
        self.url_provider.create_url_for.assert_called_with('user.user_reset', external=True, token=token)

    def test_send_reset_password_link_creates_email_body_containing_the_reset_link(self):
        # Givenfrom_the_given_email
        url = 'link'
        self.url_provider.create_url_for.return_value = url
    
        # When
        self.controller.send_reset_password_link(self.email)
    
        # Then
        self.template_provider.render_template.assert_called_with('email/reset_password.html', reset_url=url)

    def test_send_reset_password_link_sends_mail_to_the_given_address(self):
        # Given
        body = 'body'
        self.template_provider.render_template.return_value = body
    
        expected_msg_template = MsgTemplate(
            subject='Password reset requested',
            html=body,
            recipients=[self.email]
        )
    
        # When
        self.controller.send_reset_password_link(self.email)
    
        # Then
        self.mail_provider.send.assert_called_with(expected_msg_template)
