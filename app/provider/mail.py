from collections import namedtuple

from flask_mail import Message

from app.extension import mail

MsgTemplate = namedtuple('MsgTemplate', ['subject', 'recipients', 'html'])


class MailProvider:
    def __init__(self, mail, cls_msg):
        self.mail = mail
        self.cls_msg = cls_msg
    
    def send(self, msg):
        msg = self.cls_msg(subject=msg.subject, html=msg.html, recipients=msg.recipients)
        return self.mail.send(msg)


mail_provider = MailProvider(mail, Message)
