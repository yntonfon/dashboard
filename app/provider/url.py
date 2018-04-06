from flask import url_for

USER_CONFIRM_EMAIL_API = 'user.user_confirm'


class UrlProvider:
    def __init__(self, url_for):
        self.url_for = url_for
    
    def build_url_from(self, api, external, **kwargs):
        return self.url_for(api, _external=external, **kwargs)


url_provider = UrlProvider(url_for)
