from unittest import TestCase, mock

from flask_mail import Mail, Message

from app.provider import MsgTemplate
from app.provider.mail import MailProvider


class TestMailProvider(TestCase):
    def setUp(self):
        self.payload = {
            'subject': 'mysubject',
            'recipients': ['test@test.com'],
            'html': '<b>hello my dear</b>',
        }
        self.mail = mock.create_autospec(Mail)
        self.cls_msg = mock.create_autospec(Message)
        self.mail_provider = MailProvider(self.mail, self.cls_msg)
        
    def test_send_creates_new_message_with_the_given_payload(self):
        # When
        self.mail_provider.send(MsgTemplate(**self.payload))
        
        # Then
        self.cls_msg.assert_called_with(**self.payload)
        
    def test_send_sends_the_message(self):
        # Given
        msg_to_send = 'msgtosend'
        self.cls_msg.return_value = msg_to_send
        
        # When
        self.mail_provider.send(MsgTemplate(**self.payload))
        
        # Then
        self.mail.send.assert_called_with(msg_to_send)
