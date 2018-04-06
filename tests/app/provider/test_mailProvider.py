from unittest import TestCase, mock

from flask_mail import Mail

from app.provider import MsgTemplate
from app.provider.mail import MailProvider


class TestMailProvider(TestCase):
    def test_send_sends_a_new_message(self):
        # Given
        payload = {
            'subject': 'mysubject',
            'recipients': ['test@test.com'],
            'html': '<b>hello my dear</b>',
        }
        mail = mock.create_autospec(Mail)
        mail_provider = MailProvider(mail)
        
        # When
        mail_provider.send(MsgTemplate(**payload))
        
        # Then
        mail.send_message.assert_called_with(**payload)
