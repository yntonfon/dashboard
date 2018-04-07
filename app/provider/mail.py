from collections import namedtuple

from app.extension import mail as mail_instance

MsgTemplate = namedtuple('MsgTemplate', ['subject', 'recipients', 'html'])


class MailProvider:
    def __init__(self, mail):
        self.mail = mail
    
    def send(self, msg):
        return self.mail.send_message(subject=msg.subject, html=msg.html, recipients=msg.recipients)


mail_provider = MailProvider(mail_instance)
