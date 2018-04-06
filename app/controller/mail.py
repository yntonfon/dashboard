from app.provider import (security_provider as security_provider_instance,
                          url_provider as url_provider_instance,
                          template_provider as template_provider_instance,
                          mail_provider as mail_provider_instance,
                          MsgTemplate, Salt)
from app.provider.template import EMAIL_ACTIVATE_TEMPLATE
from app.provider.url import USER_CONFIRM_EMAIL_API


class MailController:
    def __init__(self, security_provider, url_provider, template_provider, mail_provider):
        self.mail_provider = mail_provider
        self.template_provider = template_provider
        self.url_provider = url_provider
        self.security_provider = security_provider
    
    def send_confirmation_email_link(self, email):
        token = self.security_provider.encrypt_to_urlsafetimed(email, salt=Salt.email_confirmation.value)
        url = self.url_provider.build_url_from(USER_CONFIRM_EMAIL_API, external=True, token=token)
        body = self.template_provider.render_template(EMAIL_ACTIVATE_TEMPLATE, confirm_url=url)
        
        msg = MsgTemplate('Confirm your email', html=body, recipients=[email])
        return self.mail_provider.send(msg)


mail_controller = MailController(security_provider_instance,
                                 url_provider_instance,
                                 template_provider_instance,
                                 mail_provider_instance)
