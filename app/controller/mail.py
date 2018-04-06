from app.provider import security_provider, url_provider, template_provider, mail_provider, MsgTemplate


class MailController:
    def __init__(self, security_provider, url_provider, template_provider, mail_provider):
        self.mail_provider = mail_provider
        self.template_provider = template_provider
        self.url_provider = url_provider
        self.security_provider = security_provider
    
    def send_confirmation_email_link(self, email):
        token = self.security_provider.encrypt_to_urlsafetimed(email, salt=security_provider.EMAIL_CONFIRMATION_LINK_KEY)
        url = self.url_provider.build_url_from(url_provider.USER_CONFIRM_EMAIL_API, external=True, token=token)
        body = self.template_provider.render_template(template_provider.EMAIL_ACTIVATE_TPL, confirm_url=url)
        
        msg = MsgTemplate('Confirm your email', html=body, recipients=[email])
        return self.mail_provider.send(msg)


mail_controller = MailController(security_provider, url_provider, template_provider, mail_provider)
