from enum import Enum

from flask import url_for


class UrlEnum(Enum):
    user_confirm_email_api = 'user.user_confirm'
    user_reset_password_api = 'user.user_reset'


class UrlProvider:
    def __init__(self, url_for):
        self.url_for = url_for

    def create_url_for(self, api, external, **kwargs):
        return self.url_for(api, _external=external, **kwargs)


url_provider = UrlProvider(url_for)
