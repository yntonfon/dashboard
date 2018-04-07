from app.provider import (security_provider as security_provider_instance,
                          url_provider as url_provider_instance,
                          template_provider as template_provider_instance,
                          mail_provider as mail_provider_instance,
                          MsgTemplate, SaltEnum, TemplateEnum, UrlEnum)


class MailController:
    def __init__(self, security_provider, url_provider, template_provider, mail_provider):
        self.mail_provider = mail_provider
        self.template_provider = template_provider
        self.url_provider = url_provider
        self.security_provider = security_provider

    def send_confirmation_link(self, email):
        token = self.security_provider.encrypt_to_urlsafetimed(email, salt=SaltEnum.email_confirmation.value)
        url = self.url_provider.create_url_for(UrlEnum.user_confirm_email_api.value, external=True, token=token)
        body = self.template_provider.render_template(TemplateEnum.email_activate.value, confirm_url=url)
        
        msg = MsgTemplate('Confirm your email', html=body, recipients=[email])
        return self.mail_provider.send(msg)

    def send_reset_password_link(self, email):
        token = self.security_provider.encrypt_to_urlsafetimed(email, salt=SaltEnum.reset_password.value)
        url = self.url_provider.create_url_for(UrlEnum.user_reset_password_api.value, external=True, token=token)
        body = self.template_provider.render_template(TemplateEnum.reset_password.value, reset_url=url)
    
        msg = MsgTemplate('Password reset requested', html=body, recipients=[email])
        return self.mail_provider.send(msg)


mail_controller = MailController(security_provider_instance,
                                 url_provider_instance,
                                 template_provider_instance,
                                 mail_provider_instance)
